from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from .serializer import (
    ProductSerializer, CategorySerializer, OrderSerializer, OrderDetailsSerializer,
    ShoppCartSerializer, ShoppCartDetailsSerializer, ReviewsSerializer,
    ServiceCategorySerializer, ServiceSerializer, ProjectSerializer, QuoteRequestSerializer,
    PaymentSerializer, ProjectMessageSerializer
)
from .models import (
    Product, Category, Order, OrderDetails, ShoppCart, ShoppCartDetails, Reviews,
    ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage
)
from user_control.models import Users
from user_control.permissions import IsAdminUserCustom, IsAdmin, IsDesigner, IsProjectParticipant

# class UserSerializerView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()


class ProductSerializerView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminUserCustom()]
        return super().get_permissions()


class CategorySerializerView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class OrderSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class OrderDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()

class ShoppCartSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartSerializer
    queryset = ShoppCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class ShoppCartDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartDetailsSerializer
    queryset = ShoppCartDetails.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class ReviewsSerializerView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]


class QuoteRequestViewSet(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.select_related('client', 'service').all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admin ve todas; cliente solo propias; diseñador opcionalmente ninguna
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            return self.queryset
        return self.queryset.filter(client=user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def approve(self, request, pk=None):
        quote = self.get_object()
        price = request.data.get('price')
        assigned_to = request.data.get('assigned_to')
        if not price:
            return Response({'detail': 'price es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            price_val = float(price)
        except ValueError:
            return Response({'detail': 'price inválido'}, status=status.HTTP_400_BAD_REQUEST)

        quote.status = 'approved'
        quote.approved_by = request.user
        quote.approved_at = timezone.now()
        quote.save()

        # Crear proyecto
        assigned_user = None
        if assigned_to:
            assigned_user = get_object_or_404(Users, id=assigned_to)

        project = Project.objects.create(
            title=quote.title,
            brief=quote.description,
            status='payment_pending',
            total_price=price_val,
            paid_amount=0,
            client=quote.client,
            assigned_to=assigned_user,
            service=quote.service
        )
        quote.linked_project = project
        quote.save()
        return Response({
            'quote': QuoteRequestSerializer(quote).data,
            'project': ProjectSerializer(project).data,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def reject(self, request, pk=None):
        quote = self.get_object()
        reason = request.data.get('rejected_reason')
        if not reason:
            return Response({'detail': 'rejected_reason es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        quote.status = 'rejected'
        quote.rejected_reason = reason
        quote.approved_by = request.user
        quote.approved_at = timezone.now()
        quote.save()
        return Response(QuoteRequestSerializer(quote).data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('client', 'assigned_to', 'service').all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            return self.queryset
        if hasattr(user, 'is_designer') and user.is_designer():
            return self.queryset.filter(assigned_to=user)
        # cliente
        return self.queryset.filter(client=user)

    def perform_create(self, serializer):
        # Si un cliente crea proyecto directo, forzar status='quote'
        user = self.request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            serializer.save(client=user)
        else:
            serializer.save(client=user, status='quote')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def assign_designer(self, request, pk=None):
        project = self.get_object()
        designer_id = request.data.get('designer_id')
        if not designer_id:
            return Response({'detail': 'designer_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            designer = Users.objects.get(id=designer_id)
        except Users.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar que el usuario sea un diseñador
        if not designer.is_designer():
            return Response({'detail': 'El usuario debe tener rol de diseñador'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Asignar diseñador y actualizar estado del proyecto
        project.assigned_to = designer
        if project.status == 'quote':
            project.status = 'in_progress'
            project.start_date = timezone.now().date()
        project.save()
        
        return Response({
            'message': f'Diseñador {designer.username} asignado al proyecto exitosamente',
            'project': ProjectSerializer(project).data
        })


class ProjectMessageViewSet(viewsets.ModelViewSet):
    queryset = ProjectMessage.objects.select_related('project', 'sender').all()
    serializer_class = ProjectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        # Filtro por project si viene query param
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            return qs
        # filtrar por participación
        return qs.filter(Q(project__client=user) | Q(project__assigned_to=user))

    def perform_create(self, serializer):
        # requiere project en body y que sea participante o admin
        project = get_object_or_404(Project, id=self.request.data.get('project'))
        user = self.request.user
        is_admin = hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin)
        if not is_admin and project.client_id != user.id and (project.assigned_to_id or 0) != user.id:
            raise permissions.PermissionDenied('No autorizado para comentar en este proyecto')
        serializer.save(sender=user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('project').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            return self.queryset
        # diseñador: pagos de asignados; cliente: de sus proyectos
        if hasattr(user, 'is_designer') and user.is_designer():
            return self.queryset.filter(project__assigned_to=user)
        return self.queryset.filter(project__client=user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def simulate(self, request):
        project_id = request.data.get('project_id')
        amount = request.data.get('amount')
        cardholder_name = request.data.get('cardholder_name', '')
        card_last4 = request.data.get('card_last4', '')
        if not project_id or not amount:
            return Response({'detail': 'project_id y amount son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, id=project_id)

        user = request.user
        is_admin = hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin)
        if not (is_admin or project.client_id == user.id):
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        try:
            amount_val = float(amount)
        except ValueError:
            return Response({'detail': 'amount inválido'}, status=status.HTTP_400_BAD_REQUEST)
        if amount_val <= 0:
            return Response({'detail': 'amount debe ser > 0'}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            project=project,
            amount=amount_val,
            status='completed',
            is_simulated=True,
            cardholder_name=cardholder_name,
            card_last4=card_last4[:4]
        )
        # actualizar proyecto
        project.paid_amount = (project.paid_amount or 0) + amount_val
        if project.status in ['payment_pending', 'approved'] and project.paid_amount >= float(project.total_price):
            project.status = 'in_progress'
        project.save()
        return Response({
            'project': ProjectSerializer(project).data,
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)