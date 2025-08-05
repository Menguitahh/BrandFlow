from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product, Category, Order, OrderDetails, ShoppCart, ShoppCartDetails, Reviews, Branch, StockMovement
from decimal import Decimal
import json

User = get_user_model()


class BrandControlTestCase(APITestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear usuario admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            roles='admin'
        )
        
        # Crear usuario cliente
        self.client_user = User.objects.create_user(
            username='cliente',
            email='cliente@test.com',
            password='cliente123',
            roles='cliente'
        )
        
        # Crear categoría
        self.category = Category.objects.create(
            name='Electrónicos',
            description='Productos electrónicos'
        )
        
        # Crear productos
        self.product1 = Product.objects.create(
            name='Laptop',
            description='Laptop de alta calidad',
            price=Decimal('999.99'),
            stock=10,
            category='Electrónicos'
        )
        
        self.product2 = Product.objects.create(
            name='Mouse',
            description='Mouse inalámbrico',
            price=Decimal('29.99'),
            stock=50,
            category='Electrónicos'
        )
        
        self.client = APIClient()


class UserRegistrationTest(APITestCase):
    """Pruebas para el registro de usuarios"""
    
    def test_user_registration(self):
        """Probar que un usuario puede registrarse correctamente"""
        url = reverse('register-list')
        data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@test.com',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'roles': 'admin'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())


class UserLoginTest(APITestCase):
    """Pruebas para el login de usuarios"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            roles='cliente'
        )
        self.url = reverse('login')
    
    def test_user_login_success(self):
        """Probar login exitoso"""
        data = {
            'identifier': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
    
    def test_user_login_failure(self):
        """Probar login fallido"""
        data = {
            'identifier': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductCRUDTest(BrandControlTestCase):
    """Pruebas CRUD para productos"""
    
    def test_create_product_as_admin(self):
        """Probar creación de producto como admin"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('Product-list')
        data = {
            'name': 'Nuevo Producto',
            'description': 'Descripción del producto',
            'price': '49.99',
            'stock': 25,
            'category': 'Electrónicos'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Nuevo Producto').exists())
    
    def test_list_products(self):
        """Probar listado de productos"""
        # Los productos son públicos, no requieren autenticación
        url = reverse('Product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_product_detail(self):
        """Probar obtener detalle de producto"""
        # Los productos son públicos, no requieren autenticación
        url = reverse('Product-detail', args=[self.product1.idproduct])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')


class StockManagementTest(BrandControlTestCase):
    """Pruebas para el manejo de stock"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_update_stock_increase(self):
        """Probar aumentar stock de producto"""
        url = reverse('Product-update-stock', args=[self.product1.idproduct])
        data = {
            'quantity': 5,
            'operation': 'increase',
            'reason': 'Reposición de inventario'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el stock se actualizó
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 15)
    
    def test_update_stock_decrease(self):
        """Probar disminuir stock de producto"""
        url = reverse('Product-update-stock', args=[self.product1.idproduct])
        data = {
            'quantity': 3,
            'operation': 'decrease',
            'reason': 'Venta'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el stock se actualizó
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 7)
    
    def test_update_stock_insufficient(self):
        """Probar disminuir stock cuando no hay suficiente"""
        url = reverse('Product-update-stock', args=[self.product1.idproduct])
        data = {
            'quantity': 15,
            'operation': 'decrease',
            'reason': 'Venta'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_low_stock_products(self):
        """Probar obtener productos con stock bajo"""
        # Crear producto con stock bajo
        Product.objects.create(
            name='Producto Stock Bajo',
            description='Producto con poco stock',
            price=Decimal('19.99'),
            stock=3,
            category='Electrónicos'
        )
        
        url = reverse('Product-low-stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_out_of_stock_products(self):
        """Probar obtener productos sin stock"""
        # Crear producto sin stock
        Product.objects.create(
            name='Producto Sin Stock',
            description='Producto sin stock',
            price=Decimal('9.99'),
            stock=0,
            category='Electrónicos'
        )
        
        url = reverse('Product-out-of-stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ShoppingCartTest(BrandControlTestCase):
    """Pruebas para el carrito de compras"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.client_user)
    
    def test_add_product_to_cart(self):
        """Probar agregar producto al carrito"""
        url = reverse('shoppcartdetails-list')
        data = {
            'idproduct': self.product1.idproduct,
            'quantity': 2
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó el carrito y el detalle
        self.assertTrue(ShoppCart.objects.filter(user=self.client_user).exists())
        self.assertTrue(ShoppCartDetails.objects.filter(
            idproduct=self.product1,
            idshoppcart__user=self.client_user
        ).exists())
    
    def test_add_product_insufficient_stock(self):
        """Probar agregar producto sin stock suficiente"""
        url = reverse('shoppcartdetails-list')
        data = {
            'idproduct': self.product1.idproduct,
            'quantity': 15  # Más del stock disponible
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_cart_details(self):
        """Probar obtener detalles del carrito"""
        # Crear carrito y agregar producto
        cart = ShoppCart.objects.create(user=self.client_user)
        ShoppCartDetails.objects.create(
            idproduct=self.product1,
            idshoppcart=cart,
            quantity=1
        )
        
        url = reverse('shoppcartdetails-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_clear_cart(self):
        """Probar vaciar carrito"""
        # Crear carrito y agregar producto
        cart = ShoppCart.objects.create(user=self.client_user)
        ShoppCartDetails.objects.create(
            idproduct=self.product1,
            idshoppcart=cart,
            quantity=1
        )
        
        url = reverse('shoppcart-clear-cart', args=[cart.idshoppcart])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el carrito está vacío
        self.assertEqual(cart.shoppcartdetails_set.count(), 0)


class OrderCreationTest(BrandControlTestCase):
    """Pruebas para la creación de órdenes"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.client_user)
        
        # Crear carrito con productos
        self.cart = ShoppCart.objects.create(user=self.client_user)
        ShoppCartDetails.objects.create(
            idproduct=self.product1,
            idshoppcart=self.cart,
            quantity=2
        )
        ShoppCartDetails.objects.create(
            idproduct=self.product2,
            idshoppcart=self.cart,
            quantity=1
        )
    
    def test_create_order_from_cart(self):
        """Probar crear orden desde el carrito"""
        url = reverse('shoppcart-create-order', args=[self.cart.idshoppcart])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertIn('total', response.data)
        
        # Verificar que se creó la orden
        order = Order.objects.get(idorder=response.data['order_id'])
        self.assertEqual(order.user, self.client_user)
        self.assertEqual(order.status, 'pending')
        
        # Verificar que se crearon los detalles de orden
        self.assertEqual(order.orderdetails_set.count(), 2)
        
        # Verificar que el stock se actualizó
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 8)  # 10 - 2
        self.assertEqual(self.product2.stock, 49)  # 50 - 1
    
    def test_create_order_empty_cart(self):
        """Probar crear orden con carrito vacío"""
        # Vaciar carrito
        self.cart.clear_cart()
        
        url = reverse('shoppcart-create-order', args=[self.cart.idshoppcart])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cancel_order(self):
        """Probar cancelar orden"""
        # Crear orden
        order = Order.objects.create(
            user=self.client_user,
            status='pending'
        )
        OrderDetails.objects.create(
            idproduct=self.product1,
            idorder=order,
            quantity=1,
            price=self.product1.price
        )
        
        # Actualizar stock inicial para la prueba
        self.product1.stock = 5
        self.product1.save()
        
        url = reverse('Order-cancel-order', args=[order.idorder])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la orden se canceló
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')
        
        # Verificar que el stock se restauró
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 6)  # 5 + 1


class StockMovementTest(BrandControlTestCase):
    """Pruebas para movimientos de stock"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_stock_movement_creation(self):
        """Probar que se crean registros de movimientos de stock"""
        url = reverse('Product-update-stock', args=[self.product1.idproduct])
        data = {
            'quantity': 5,
            'operation': 'increase',
            'reason': 'Reposición'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se creó el movimiento
        movement = StockMovement.objects.filter(product=self.product1).first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.movement_type, 'increase')
        self.assertEqual(movement.quantity, 5)
        self.assertEqual(movement.reason, 'Reposición')
    
    def test_get_stock_movements(self):
        """Probar obtener movimientos de stock"""
        # Crear algunos movimientos
        StockMovement.objects.create(
            product=self.product1,
            movement_type='increase',
            quantity=10,
            previous_stock=0,
            new_stock=10,
            reason='Stock inicial',
            user=self.admin_user
        )
        
        url = reverse('StockMovement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ReviewTest(BrandControlTestCase):
    """Pruebas para reviews"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.client_user)
    
    def test_create_review(self):
        """Probar crear review"""
        url = reverse('Reviews-list')
        data = {
            'idproduct': self.product1.idproduct,
            'rating': 5,
            'comment': 'Excelente producto'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó la review
        review = Reviews.objects.filter(
            idproduct=self.product1,
            user=self.client_user
        ).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excelente producto')


class BranchTest(BrandControlTestCase):
    """Pruebas para sucursales"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_create_branch(self):
        """Probar crear sucursal"""
        url = reverse('Branch-list')
        data = {
            'name': 'Sucursal Centro',
            'address': 'Calle Principal 123',
            'phone': '123456789'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó la sucursal
        branch = Branch.objects.filter(name='Sucursal Centro').first()
        self.assertIsNotNone(branch)
        self.assertEqual(branch.company, self.admin_user)


class IntegrationTest(BrandControlTestCase):
    """Pruebas de integración del flujo completo"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.client_user)
    
    def test_complete_purchase_flow(self):
        """Probar el flujo completo de compra"""
        # 1. Agregar productos al carrito
        cart_url = reverse('shoppcartdetails-list')
        cart_data1 = {
            'idproduct': self.product1.idproduct,
            'quantity': 1
        }
        cart_data2 = {
            'idproduct': self.product2.idproduct,
            'quantity': 2
        }
        
        self.client.post(cart_url, cart_data1)
        self.client.post(cart_url, cart_data2)
        
        # Verificar que se agregaron al carrito
        cart = ShoppCart.objects.get(user=self.client_user)
        self.assertEqual(cart.shoppcartdetails_set.count(), 2)
        
        # 2. Crear orden desde el carrito
        order_url = reverse('shoppcart-create-order', args=[cart.idshoppcart])
        response = self.client.post(order_url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. Verificar que se creó la orden correctamente
        order = Order.objects.get(idorder=response.data['order_id'])
        self.assertEqual(order.user, self.client_user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.orderdetails_set.count(), 2)
        
        # 4. Verificar que el stock se actualizó
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 9)  # 10 - 1
        self.assertEqual(self.product2.stock, 48)  # 50 - 2
        
        # 5. Verificar que se crearon movimientos de stock
        movements = StockMovement.objects.filter(product__in=[self.product1, self.product2])
        self.assertEqual(movements.count(), 2)
        
        # 6. Cancelar la orden
        cancel_url = reverse('Order-cancel-order', args=[order.idorder])
        cancel_response = self.client.post(cancel_url)
        
        self.assertEqual(cancel_response.status_code, status.HTTP_200_OK)
        
        # 7. Verificar que el stock se restauró
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 10)  # 9 + 1
        self.assertEqual(self.product2.stock, 50)  # 48 + 2
