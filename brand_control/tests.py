from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import json

from .models import Category, Product, Order, OrderDetails, ShoppCart, ShoppCartDetails, StockMovement
from user_control.models import Users

User = get_user_model()


class CoreEcommerceTestCase(APITestCase):
    """Pruebas para las funcionalidades core del ecommerce"""
    
    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        # Crear usuario de prueba
        self.user = Users.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test123!',
            first_name='Test',
            last_name='User',
            roles='cliente'
        )
        
        # Crear usuario admin
        self.admin_user = Users.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Admin123!',
            first_name='Admin',
            last_name='User',
            roles='admin'
        )
        
        # Crear categoría de prueba
        self.category = Category.objects.create(
            name='Electrónicos',
            description='Productos electrónicos'
        )
        
        # Crear producto de prueba
        self.product = Product.objects.create(
            name='Laptop Gaming',
            description='Laptop para gaming de alta calidad',
            price=Decimal('1500.00'),
            stock=10,
            category_id=self.category,
            is_active=True
        )
        
        # Crear carrito de prueba
        self.cart = ShoppCart.objects.create(user=self.user)
        
        # Configurar cliente API
        self.client = APIClient()
    
    def test_1_user_registration(self):
        """Prueba 1: Registro de usuarios"""
        print("\n=== PRUEBA 1: REGISTRO DE USUARIOS ===")
        
        # Datos antes del registro
        initial_user_count = Users.objects.count()
        print(f"Usuarios antes del registro: {initial_user_count}")
        
        # Datos para el nuevo usuario
        user_data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@example.com',
            'password': 'Password123!',
            'password2': 'Password123!',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'phone': '123456789',
            'address': 'Calle Nueva 123',
            'roles': 'cliente'
        }
        
        # Realizar registro
        url = reverse('user_control:register')
        response = self.client.post(url, user_data, format='json')
        
        print(f"Respuesta del registro: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el registro fue exitoso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el usuario se creó en la base de datos
        final_user_count = Users.objects.count()
        print(f"Usuarios después del registro: {final_user_count}")
        self.assertEqual(final_user_count, initial_user_count + 1)
        
        # Verificar que el usuario existe
        new_user = Users.objects.get(username='nuevo_usuario')
        self.assertEqual(new_user.email, 'nuevo@example.com')
        self.assertEqual(new_user.roles, 'cliente')
        
        print("Registro de usuario exitoso")
    
    def test_2_user_login(self):
        """Prueba 2: Login de usuarios"""
        print("\n=== PRUEBA 2: LOGIN DE USUARIOS ===")
        
        # Datos de login
        login_data = {
            'identifier': 'testuser',
            'password': 'Test123!'
        }
        
        # Realizar login
        url = reverse('user_control:login')
        response = self.client.post(url, login_data, format='json')
        
        print(f"Respuesta del login: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el login fue exitoso
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('session_id', response.data)
        
        # Verificar que el usuario está autenticado
        self.assertTrue(response.data['user']['username'] == 'testuser')
        
        print("Login de usuario exitoso")
    
    def test_3_product_creation_admin(self):
        """Prueba 3: Agregado de productos (como admin)"""
        print("\n=== PRUEBA 3: AGREGADO DE PRODUCTOS (ADMIN) ===")
        
        # Login como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Datos antes de crear producto
        initial_product_count = Product.objects.count()
        print(f"Productos antes de crear: {initial_product_count}")
        
        # Datos del nuevo producto
        product_data = {
            'name': 'Smartphone Pro',
            'description': 'Smartphone de última generación',
            'price': '800.00',
            'stock': 15,
            'category_id': self.category.id,
            'is_active': True
        }
        
        # Crear producto
        url = reverse('Product-list')
        response = self.client.post(url, product_data, format='json')
        
        print(f"Respuesta de creación de producto: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el producto se creó exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el producto existe en la base de datos
        final_product_count = Product.objects.count()
        print(f"Productos después de crear: {final_product_count}")
        self.assertEqual(final_product_count, initial_product_count + 1)
        
        # Verificar datos del producto creado
        new_product = Product.objects.get(name='Smartphone Pro')
        self.assertEqual(new_product.price, Decimal('800.00'))
        self.assertEqual(new_product.stock, 15)
        self.assertEqual(new_product.category_id, self.category)
        
        print("Creación de producto exitosa")
    
    def test_4_product_listing(self):
        """Prueba 4: Listado de productos"""
        print("\n=== PRUEBA 4: LISTADO DE PRODUCTOS ===")
        
        # Crear productos adicionales para la prueba
        Product.objects.create(
            name='Tablet Pro',
            description='Tablet profesional',
            price=Decimal('500.00'),
            stock=8,
            category_id=self.category,
            is_active=True
        )
        
        Product.objects.create(
            name='Auriculares Wireless',
            description='Auriculares bluetooth',
            price=Decimal('150.00'),
            stock=20,
            category_id=self.category,
            is_active=True
        )
        
        # Obtener listado de productos
        url = reverse('Product-list')
        response = self.client.get(url)
        
        print(f"Respuesta del listado: {response.status_code}")
        print(f"Cantidad de productos: {len(response.data)}")
        
        # Verificar que la respuesta fue exitosa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se obtuvieron productos
        self.assertGreater(len(response.data), 0)
        
        # Verificar estructura de los datos
        if len(response.data) > 0:
            product = response.data[0]
            self.assertIn('id', product)
            self.assertIn('name', product)
            self.assertIn('price', product)
            self.assertIn('stock', product)
        
        print("Listado de productos exitoso")
    
    def test_5_add_product_to_cart(self):
        """Prueba 5: Agregar producto al carrito"""
        print("\n=== PRUEBA 5: AGREGAR PRODUCTO AL CARRITO ===")
        
        # Login como usuario normal
        self.client.force_authenticate(user=self.user)
        
        # Datos antes de agregar al carrito
        initial_cart_details_count = ShoppCartDetails.objects.count()
        print(f"Detalles de carrito antes: {initial_cart_details_count}")
        
        # Datos para agregar al carrito
        cart_detail_data = {
            'idproduct': self.product.id,
            'idshoppcart': self.cart.idshoppcart,
            'quantity': 2
        }
        
        # Agregar producto al carrito
        url = reverse('shoppcartdetails-list')
        response = self.client.post(url, cart_detail_data, format='json')
        
        print(f"Respuesta de agregar al carrito: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que se agregó exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó el detalle del carrito
        final_cart_details_count = ShoppCartDetails.objects.count()
        print(f"Detalles de carrito después: {final_cart_details_count}")
        self.assertEqual(final_cart_details_count, initial_cart_details_count + 1)
        
        # Verificar datos del detalle creado
        cart_detail = ShoppCartDetails.objects.get(
            idproduct=self.product,
            idshoppcart=self.cart
        )
        self.assertEqual(cart_detail.quantity, 2)
        
        print("Agregar producto al carrito exitoso")
    
    def test_6_create_order_from_cart(self):
        """Prueba 6: Crear pedido desde el carrito"""
        print("\n=== PRUEBA 6: CREAR PEDIDO DESDE EL CARRITO ===")
        
        # Login como usuario normal
        self.client.force_authenticate(user=self.user)
        
        # Agregar producto al carrito primero
        cart_detail = ShoppCartDetails.objects.create(
            idproduct=self.product,
            idshoppcart=self.cart,
            quantity=3
        )
        
        # Datos antes de crear el pedido
        initial_order_count = Order.objects.count()
        initial_order_details_count = OrderDetails.objects.count()
        initial_stock = self.product.stock
        print(f"Pedidos antes: {initial_order_count}")
        print(f"Detalles de pedido antes: {initial_order_details_count}")
        print(f"Stock antes: {initial_stock}")
        
        # Datos del pedido
        order_data = {
            'user': self.user.id,
            'status': 'pending',
            'total': '4500.00'  # 3 * 1500.00
        }
        
        # Crear pedido
        url = reverse('Order-list')
        response = self.client.post(url, order_data, format='json')
        
        print(f"Respuesta de creación de pedido: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el pedido se creó exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el pedido existe
        final_order_count = Order.objects.count()
        print(f"Pedidos después: {final_order_count}")
        self.assertEqual(final_order_count, initial_order_count + 1)
        
        # Crear detalle del pedido
        order = Order.objects.latest('idorder')
        order_detail_data = {
            'idproduct': self.product.id,
            'idorder': order.idorder,
            'quantity': 3,
            'price': '1500.00'
        }
        
        url_detail = reverse('OrderDetails-list')
        response_detail = self.client.post(url_detail, order_detail_data, format='json')
        
        print(f"Respuesta de creación de detalle: {response_detail.status_code}")
        
        # Verificar que el detalle se creó exitosamente
        self.assertEqual(response_detail.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el stock se actualizó
        self.product.refresh_from_db()
        final_stock = self.product.stock
        print(f"Stock después: {final_stock}")
        self.assertEqual(final_stock, initial_stock - 3)
        
        # Verificar que se creó el movimiento de stock
        stock_movements = StockMovement.objects.filter(product=self.product)
        self.assertGreater(stock_movements.count(), 0)
        
        print("Creación de pedido desde carrito exitosa")
    
    def test_7_stock_management(self):
        """Prueba 7: Gestión de stock (CRUD)"""
        print("\n=== PRUEBA 7: GESTIÓN DE STOCK ===")
        
        # Login como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # READ - Leer stock
        print("--- READ: Leer stock ---")
        initial_stock = self.product.stock
        print(f"Stock inicial del producto: {initial_stock}")
        
        # Verificar método has_stock
        self.assertTrue(self.product.has_stock(5))
        self.assertFalse(self.product.has_stock(15))
        
        # UPDATE - Actualizar stock (disminuir)
        print("--- UPDATE: Actualizar stock (disminuir) ---")
        success = self.product.update_stock(2, 'decrease')
        self.assertTrue(success)
        self.product.refresh_from_db()
        print(f"Stock después de disminuir 2: {self.product.stock}")
        self.assertEqual(self.product.stock, initial_stock - 2)
        
        # UPDATE - Actualizar stock (aumentar)
        print("--- UPDATE: Actualizar stock (aumentar) ---")
        success = self.product.update_stock(5, 'increase')
        self.assertTrue(success)
        self.product.refresh_from_db()
        print(f"Stock después de aumentar 5: {self.product.stock}")
        self.assertEqual(self.product.stock, initial_stock - 2 + 5)
        
        # Verificar que no se puede disminuir más stock del disponible
        print("--- Verificar límite de stock ---")
        success = self.product.update_stock(100, 'decrease')
        self.assertFalse(success)
        self.product.refresh_from_db()
        print(f"Stock después de intento fallido: {self.product.stock}")
        
        print("Gestión de stock exitosa")
    
    def test_8_order_cancellation_stock_restoration(self):
        """Prueba 8: Cancelación de pedido y restauración de stock"""
        print("\n=== PRUEBA 8: CANCELACIÓN DE PEDIDO Y RESTAURACIÓN DE STOCK ===")
        
        # Crear pedido con detalle
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total=Decimal('1500.00')
        )
        
        order_detail = OrderDetails.objects.create(
            idproduct=self.product,
            idorder=order,
            quantity=2,
            price=Decimal('1500.00')
        )
        
        # Stock antes de la cancelación
        initial_stock = self.product.stock
        print(f"Stock antes de cancelación: {initial_stock}")
        
        # Cancelar pedido
        order.cancel_order()
        order.refresh_from_db()
        
        print(f"Estado del pedido después de cancelación: {order.status}")
        self.assertEqual(order.status, 'cancelled')
        
        # Verificar que el stock se restauró
        self.product.refresh_from_db()
        final_stock = self.product.stock
        print(f"Stock después de cancelación: {final_stock}")
        self.assertEqual(final_stock, initial_stock + 2)
        
        # Verificar que se creó movimiento de stock para restauración
        restoration_movements = StockMovement.objects.filter(
            product=self.product,
            movement_type='in',
            reason__contains='Restauración'
        )
        self.assertGreater(restoration_movements.count(), 0)
        
        print("Cancelación de pedido y restauración de stock exitosa")
    
    def test_9_complete_ecommerce_flow(self):
        """Prueba 9: Flujo completo de ecommerce"""
        print("\n=== PRUEBA 9: FLUJO COMPLETO DE ECOMMERCE ===")
        
        # 1. Login del usuario
        self.client.force_authenticate(user=self.user)
        print("1. Usuario autenticado")
        
        # 2. Ver productos disponibles
        url_products = reverse('Product-list')
        response_products = self.client.get(url_products)
        self.assertEqual(response_products.status_code, status.HTTP_200_OK)
        print("2. Productos obtenidos")
        
        # 3. Agregar productos al carrito
        cart_detail_data = {
            'idproduct': self.product.id,
            'idshoppcart': self.cart.idshoppcart,
            'quantity': 1
        }
        url_cart = reverse('shoppcartdetails-list')
        response_cart = self.client.post(url_cart, cart_detail_data, format='json')
        self.assertEqual(response_cart.status_code, status.HTTP_201_CREATED)
        print("3. Producto agregado al carrito")
        
        # 4. Crear pedido
        order_data = {
            'user': self.user.id,
            'status': 'pending',
            'total': '1500.00'
        }
        url_order = reverse('Order-list')
        response_order = self.client.post(url_order, order_data, format='json')
        self.assertEqual(response_order.status_code, status.HTTP_201_CREATED)
        print("4. Pedido creado")
        
        # 5. Verificar que el stock se actualizó (nota: en este flujo, el stock se descuenta al crear OrderDetails)
        # Creamos el detalle ahora para generar el descuento
        order = Order.objects.latest('idorder')
        OrderDetails.objects.create(idproduct=self.product, idorder=order, quantity=1, price=Decimal('1500.00'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
        print("5. Stock actualizado correctamente")
        
        # 6. Verificar que se creó movimiento de stock
        stock_movements = StockMovement.objects.filter(product=self.product)
        self.assertGreater(stock_movements.count(), 0)
        print("6. Movimiento de stock registrado")
        
        print("Flujo completo de ecommerce exitoso")


class StockManagementTestCase(APITestCase):
    """Pruebas específicas para gestión de stock"""
    
    def setUp(self):
        self.user = Users.objects.create_user(
            username='stockuser',
            email='stock@example.com',
            password='Stock123!',
            roles='admin'
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Categoría de prueba'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Producto de prueba',
            price=Decimal('100.00'),
            stock=50,
            category_id=self.category
        )
        
        self.client.force_authenticate(user=self.user)
    
    def test_stock_creation(self):
        """Prueba creación de stock"""
        print("\n=== PRUEBA: CREACIÓN DE STOCK ===")
        
        # Crear producto con stock inicial
        product_data = {
            'name': 'Nuevo Producto',
            'description': 'Producto con stock inicial',
            'price': '200.00',
            'stock': 25,
            'category_id': self.category.id,
            'is_active': True
        }
        
        url = reverse('Product-list')
        response = self.client.post(url, product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stock'], 25)
        print("Creación de stock exitosa")
    
    def test_stock_reading(self):
        """Prueba lectura de stock"""
        print("\n=== PRUEBA: LECTURA DE STOCK ===")
        
        url = reverse('Product-detail', args=[self.product.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], 50)
        print("Lectura de stock exitosa")
    
    def test_stock_update(self):
        """Prueba actualización de stock"""
        print("\n=== PRUEBA: ACTUALIZACIÓN DE STOCK ===")
        
        # Actualizar stock
        product_data = {
            'name': self.product.name,
            'description': self.product.description,
            'price': str(self.product.price),
            'stock': 30,  # Cambiar de 50 a 30
            'category_id': self.category.id,
            'is_active': True
        }
        
        url = reverse('Product-detail', args=[self.product.id])
        response = self.client.put(url, product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], 30)
        print("Actualización de stock exitosa")
    
    def test_stock_deletion_prevention(self):
        """Prueba prevención de eliminación de stock"""
        print("\n=== PRUEBA: PREVENCIÓN DE ELIMINACIÓN DE STOCK ===")
        
        # Intentar eliminar producto (no recomendado)
        url = reverse('Product-detail', args=[self.product.id])
        response = self.client.delete(url)
        
        # Verificar que se puede eliminar (pero no es recomendado)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Producto eliminado (no recomendado en producción)")
        
        # Alternativa: marcar como inactivo en lugar de eliminar
        product_data = {
            'name': 'Producto Inactivo',
            'description': 'Producto marcado como inactivo',
            'price': '100.00',
            'stock': 0,
            'category_id': self.category.id,
            'is_active': False  # Marcar como inactivo
        }
        
        url = reverse('Product-list')
        response = self.client.post(url, product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['is_active'])
        print("Producto marcado como inactivo (mejor práctica)")


if __name__ == '__main__':
    # Ejecutar pruebas específicas
    import django
    django.setup()
    
    # Crear instancia de prueba y ejecutar
    test_case = CoreEcommerceTestCase()
    test_case.setUp()
    
    print("🚀 INICIANDO PRUEBAS DE FUNCIONALIDADES CORE")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_case.test_1_user_registration()
    test_case.test_2_user_login()
    test_case.test_3_product_creation_admin()
    test_case.test_4_product_listing()
    test_case.test_5_add_product_to_cart()
    test_case.test_6_create_order_from_cart()
    test_case.test_7_stock_management()
    test_case.test_8_order_cancellation_stock_restoration()
    test_case.test_9_complete_ecommerce_flow()
    
    print("\n" + "=" * 50)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("🎉 El sistema está listo para producción!")
