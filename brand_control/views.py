from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .serializer import *
from .models import *
from user_control.permissions import IsAdminUserCustom
from user_control.models import Users


class ProductSerializerView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    permission_classes = []  # Hacer público

    def get_queryset(self):
        """Filtrar productos por categoría si se especifica"""
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserCustom])
    def update_stock(self, request, pk=None):
        """Actualizar stock de un producto"""
        product = self.get_object()
        serializer = StockUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            operation = serializer.validated_data['operation']
            reason = serializer.validated_data['reason']
            
            # Registrar movimiento de stock
            previous_stock = product.stock
            
            if operation == 'increase':
                success = product.update_stock(quantity, 'increase')
                new_stock = product.stock
            else:  # decrease
                success = product.update_stock(quantity, 'decrease')
                new_stock = product.stock
            
            if success:
                # Crear registro de movimiento
                StockMovement.objects.create(
                    product=product,
                    movement_type=operation,
                    quantity=quantity,
                    previous_stock=previous_stock,
                    new_stock=new_stock,
                    reason=reason,
                    user=request.user
                )
                
                return Response({
                    'message': f'Stock actualizado exitosamente. Nuevo stock: {new_stock}',
                    'new_stock': new_stock
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No hay suficiente stock para realizar la operación'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Obtener productos con stock bajo"""
        products = Product.objects.filter(stock__lte=5, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Obtener productos sin stock"""
        products = Product.objects.filter(stock=0, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CategorySerializerView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class OrderSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar órdenes por usuario"""
        if self.request.user.roles == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        """Cancelar una orden"""
        order = self.get_object()
        
        if order.status == 'pending':
            if order.cancel_order():
                return Response({
                    'message': 'Orden cancelada exitosamente'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No se pudo cancelar la orden'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Solo se pueden cancelar órdenes pendientes'
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ShoppCartSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartSerializer
    queryset = ShoppCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar carritos por usuario"""
        return ShoppCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Crear carrito para el usuario actual"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def clear_cart(self, request, pk=None):
        """Vaciar carrito"""
        cart = self.get_object()
        cart.clear_cart()
        return Response({
            'message': 'Carrito vaciado exitosamente'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create_order(self, request, pk=None):
        """Crear orden desde el carrito"""
        cart = self.get_object()
        
        if not cart.shoppcartdetails_set.exists():
            return Response({
                'error': 'El carrito está vacío'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Crear orden
                order = Order.objects.create(
                    user=request.user,
                    status='pending'
                )
                
                # Crear detalles de orden
                total = 0
                for cart_detail in cart.shoppcartdetails_set.all():
                    if cart_detail.idproduct.has_stock(cart_detail.quantity):
                        OrderDetails.objects.create(
                            idproduct=cart_detail.idproduct,
                            idorder=order,
                            quantity=cart_detail.quantity,
                            price=cart_detail.idproduct.price
                        )
                        total += cart_detail.idproduct.price * cart_detail.quantity
                    else:
                        # Si no hay stock, cancelar la transacción
                        raise ValueError(f"Stock insuficiente para {cart_detail.idproduct.name}")
                
                # Actualizar total de la orden
                order.total = total
                order.save()
                
                # Vaciar carrito
                cart.clear_cart()
                
                return Response({
                    'message': 'Orden creada exitosamente',
                    'order_id': order.idorder,
                    'total': total
                }, status=status.HTTP_201_CREATED)
                
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Error al crear la orden'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShoppCartDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartDetailsSerializer
    queryset = ShoppCartDetails.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar detalles de carrito por usuario"""
        return ShoppCartDetails.objects.filter(idshoppcart__user=self.request.user)

    def perform_create(self, serializer):
        """Crear detalle de carrito"""
        # Obtener o crear carrito para el usuario
        cart, created = ShoppCart.objects.get_or_create(user=self.request.user)
        serializer.save(idshoppcart=cart)


class ReviewsSerializerView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Crear review con el usuario actual"""
        serializer.save(user=self.request.user)


class BranchSerializerView(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        """Crear sucursal con la empresa del usuario"""
        serializer.save(company=self.request.user)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """Vista de solo lectura para movimientos de stock"""
    serializer_class = StockMovementSerializer
    queryset = StockMovement.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def get_queryset(self):
        """Filtrar movimientos por producto si se especifica"""
        queryset = StockMovement.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset.order_by('-created_at')

