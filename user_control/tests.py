from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

from .models import Users
from brand_control.models import Category, Product, ShoppCart

User = get_user_model()


class UserManagementTestCase(APITestCase):
    """Pruebas para el manejo de usuarios y autenticación"""
    
    def setUp(self):
        """Configuración inicial para las pruebas de usuarios"""
        # Crear usuarios de prueba
        self.admin_user = Users.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Admin123!',
            first_name='Admin',
            last_name='User',
            roles='admin'
        )
        
        self.client_user = Users.objects.create_user(
            username='client',
            email='client@example.com',
            password='Client123!',
            first_name='Client',
            last_name='User',
            roles='cliente'
        )
        
        self.vendor_user = Users.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='Vendor123!',
            first_name='Vendor',
            last_name='User',
            roles='vendedor'
        )
        
        # Crear datos de prueba para brand_control
        self.category = Category.objects.create(
            name='Test Category',
            description='Categoría de prueba'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Producto de prueba',
            price=100.00,
            stock=10,
            category_id=self.category
        )
        
        # Configurar cliente API
        self.client = APIClient()
    
    def test_user_registration_success(self):
        """Prueba registro exitoso de usuario"""
        print("\n=== PRUEBA: REGISTRO EXITOSO DE USUARIO ===")
        
        # Datos antes del registro
        initial_count = Users.objects.count()
        print(f"Usuarios antes del registro: {initial_count}")
        
        # Datos del nuevo usuario
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewUser123!',
            'password2': 'NewUser123!',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '987654321',
            'address': 'Nueva Dirección 456',
            'roles': 'cliente'
        }
        
        # Realizar registro
        url = reverse('user_control:register')
        response = self.client.post(url, user_data, format='json')
        
        print(f"Respuesta del registro: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó el usuario
        final_count = Users.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Verificar datos del usuario creado
        new_user = Users.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertEqual(new_user.roles, 'cliente')
        self.assertTrue(new_user.check_password('NewUser123!'))
        
        print("✅ Registro de usuario exitoso")
    
    def test_user_registration_validation(self):
        """Prueba validaciones en el registro de usuarios"""
        print("\n=== PRUEBA: VALIDACIONES EN REGISTRO ===")
        
        # Prueba 1: Contraseñas no coinciden
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!',
            'password2': 'DifferentPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
            'roles': 'cliente'
        }
        
        url = reverse('user_control:register')
        response = self.client.post(url, user_data, format='json')
        
        print(f"Respuesta con contraseñas diferentes: {response.status_code}")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Prueba 2: Usuario ya existe
        user_data['password2'] = 'Password123!'
        response = self.client.post(url, user_data, format='json')
        
        print(f"Respuesta con usuario existente: {response.status_code}")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        
        print("✅ Validaciones de registro funcionando")
    
    def test_user_login_success(self):
        """Prueba login exitoso de usuario"""
        print("\n=== PRUEBA: LOGIN EXITOSO ===")
        
        # Datos de login
        login_data = {
            'identifier': 'client',
            'password': 'Client123!'
        }
        
        # Realizar login
        url = reverse('user_control:login')
        response = self.client.post(url, login_data, format='json')
        
        print(f"Respuesta del login: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('session_id', response.data)
        
        # Verificar datos del usuario
        user_data = response.data['user']
        self.assertEqual(user_data['username'], 'client')
        self.assertEqual(user_data['email'], 'client@example.com')
        self.assertEqual(user_data['roles'], 'cliente')
        
        print("✅ Login exitoso")
    
    def test_user_login_by_email(self):
        """Prueba login usando email"""
        print("\n=== PRUEBA: LOGIN POR EMAIL ===")
        
        # Login usando email
        login_data = {
            'identifier': 'client@example.com',
            'password': 'Client123!'
        }
        
        url = reverse('user_control:login')
        response = self.client.post(url, login_data, format='json')
        
        print(f"Respuesta del login por email: {response.status_code}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'client@example.com')
        
        print("✅ Login por email exitoso")
    
    def test_user_login_invalid_credentials(self):
        """Prueba login con credenciales inválidas"""
        print("\n=== PRUEBA: LOGIN CON CREDENCIALES INVÁLIDAS ===")
        
        # Prueba con contraseña incorrecta
        login_data = {
            'identifier': 'client',
            'password': 'WrongPassword123!'
        }
        
        url = reverse('user_control:login')
        response = self.client.post(url, login_data, format='json')
        
        print(f"Respuesta con contraseña incorrecta: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Prueba con usuario inexistente
        login_data = {
            'identifier': 'nonexistent',
            'password': 'AnyPassword123!'
        }
        
        response = self.client.post(url, login_data, format='json')
        
        print(f"Respuesta con usuario inexistente: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        print("✅ Validaciones de login funcionando")
    
    def test_user_logout(self):
        """Prueba logout de usuario"""
        print("\n=== PRUEBA: LOGOUT ===")
        
        # Login primero
        self.client.force_authenticate(user=self.client_user)
        
        # Realizar logout
        url = reverse('user_control:logout')
        response = self.client.post(url)
        
        print(f"Respuesta del logout: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('session_cleared', response.data)
        
        print("✅ Logout exitoso")
    
    def test_user_profile_get(self):
        """Prueba obtener perfil de usuario"""
        print("\n=== PRUEBA: OBTENER PERFIL DE USUARIO ===")
        
        # Autenticar usuario
        self.client.force_authenticate(user=self.client_user)
        
        # Obtener perfil
        url = reverse('user_control:profile')
        response = self.client.get(url)
        
        print(f"Respuesta del perfil: {response.status_code}")
        print(f"Contenido del perfil: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'client')
        self.assertEqual(response.data['email'], 'client@example.com')
        self.assertEqual(response.data['roles'], 'cliente')
        
        print("✅ Obtención de perfil exitosa")
    
    def test_user_profile_update(self):
        """Prueba actualizar perfil de usuario"""
        print("\n=== PRUEBA: ACTUALIZAR PERFIL DE USUARIO ===")
        
        # Autenticar usuario
        self.client.force_authenticate(user=self.client_user)
        
        # Datos de actualización
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '555123456',
            'address': 'Nueva Dirección Actualizada'
        }
        
        # Actualizar perfil
        url = reverse('user_control:profile')
        response = self.client.put(url, update_data, format='json')
        
        print(f"Respuesta de actualización: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        
        # Verificar que se actualizaron los datos
        updated_user = Users.objects.get(id=self.client_user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertEqual(updated_user.phone, '555123456')
        
        print("✅ Actualización de perfil exitosa")
    
    def test_session_status(self):
        """Prueba estado de sesión"""
        print("\n=== PRUEBA: ESTADO DE SESIÓN ===")
        
        # Sin autenticar
        url = reverse('user_control:session-status')
        response = self.client.get(url)
        
        print(f"Respuesta sin autenticar: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['authenticated'])
        
        # Con autenticación
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(url)
        
        print(f"Respuesta autenticado: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['authenticated'])
        self.assertIn('user', response.data)
        
        print("✅ Verificación de estado de sesión exitosa")
    
    def test_admin_create_user(self):
        """Prueba creación de usuario por admin"""
        print("\n=== PRUEBA: CREACIÓN DE USUARIO POR ADMIN ===")
        
        # Autenticar como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Datos del nuevo usuario
        user_data = {
            'username': 'newemployee',
            'email': 'employee@example.com',
            'password': 'Employee123!',
            'password2': 'Employee123!',
            'first_name': 'Employee',
            'last_name': 'User',
            'phone': '123456789',
            'address': 'Dirección del empleado',
            'roles': 'vendedor'
        }
        
        # Crear usuario
        url = reverse('user_control:admin-create-user')
        response = self.client.post(url, user_data, format='json')
        
        print(f"Respuesta de creación por admin: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar éxito
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó el usuario
        new_user = Users.objects.get(username='newemployee')
        self.assertEqual(new_user.roles, 'vendedor')
        self.assertEqual(new_user.company, self.admin_user)
        
        print("✅ Creación de usuario por admin exitosa")
    
    def test_user_roles_and_permissions(self):
        """Prueba roles y permisos de usuario"""
        print("\n=== PRUEBA: ROLES Y PERMISOS ===")
        
        # Verificar propiedades de roles
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.admin_user.is_client)
        
        self.assertTrue(self.client_user.is_client)
        self.assertFalse(self.client_user.is_admin)
        
        self.assertTrue(self.vendor_user.is_vendor)
        self.assertFalse(self.vendor_user.is_admin)
        
        # Verificar acceso a funcionalidades según rol
        self.client.force_authenticate(user=self.client_user)
        
        # Cliente no debería poder crear productos
        product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '100.00',
            'stock': 10,
            'category_id': self.category.id
        }
        
        url = reverse('Product-list')
        response = self.client.post(url, product_data, format='json')
        
        print(f"Respuesta de cliente intentando crear producto: {response.status_code}")
        # Debería ser 403 (Forbidden) porque solo admins pueden crear productos
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        print("✅ Roles y permisos funcionando correctamente")
    
    def test_user_company_relationship(self):
        """Prueba relación empresa-empleado"""
        print("\n=== PRUEBA: RELACIÓN EMPRESA-EMPLEADO ===")
        
        # Crear empleado asociado a admin
        employee = Users.objects.create_user(
            username='employee',
            email='employee@company.com',
            password='Employee123!',
            first_name='Employee',
            last_name='User',
            roles='vendedor',
            company=self.admin_user  # Asociar al admin como empresa
        )
        
        # Verificar relación
        self.assertEqual(employee.company, self.admin_user)
        self.assertIn(employee, self.admin_user.employees.all())
        
        print("✅ Relación empresa-empleado funcionando")
    
    def test_user_authentication_flow(self):
        """Prueba flujo completo de autenticación"""
        print("\n=== PRUEBA: FLUJO COMPLETO DE AUTENTICACIÓN ===")
        
        # 1. Registro de usuario
        user_data = {
            'username': 'flowuser',
            'email': 'flow@example.com',
            'password': 'Flow123!',
            'password2': 'Flow123!',
            'first_name': 'Flow',
            'last_name': 'User',
            'phone': '111222333',
            'address': 'Dirección del flujo',
            'roles': 'cliente'
        }
        
        url_register = reverse('user_control:register')
        response_register = self.client.post(url_register, user_data, format='json')
        self.assertEqual(response_register.status_code, status.HTTP_201_CREATED)
        print("1. ✅ Usuario registrado")
        
        # 2. Login del usuario
        login_data = {
            'identifier': 'flowuser',
            'password': 'Flow123!'
        }
        
        url_login = reverse('user_control:login')
        response_login = self.client.post(url_login, login_data, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        print("2. ✅ Usuario logueado")
        
        # 3. Verificar estado de sesión
        url_status = reverse('user_control:session-status')
        response_status = self.client.get(url_status)
        self.assertEqual(response_status.status_code, status.HTTP_200_OK)
        self.assertTrue(response_status.data['authenticated'])
        print("3. ✅ Estado de sesión verificado")
        
        # 4. Obtener perfil
        url_profile = reverse('user_control:profile')
        response_profile = self.client.get(url_profile)
        self.assertEqual(response_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profile.data['username'], 'flowuser')
        print("4. ✅ Perfil obtenido")
        
        # 5. Logout
        url_logout = reverse('user_control:logout')
        response_logout = self.client.post(url_logout)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        print("5. ✅ Usuario deslogueado")
        
        print("✅ Flujo completo de autenticación exitoso")


if __name__ == '__main__':
    # Ejecutar pruebas específicas
    import django
    django.setup()
    
    # Crear instancia de prueba y ejecutar
    test_case = UserManagementTestCase()
    test_case.setUp()
    
    print("🚀 INICIANDO PRUEBAS DE MANEJO DE USUARIOS")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_case.test_user_registration_success()
    test_case.test_user_registration_validation()
    test_case.test_user_login_success()
    test_case.test_user_login_by_email()
    test_case.test_user_login_invalid_credentials()
    test_case.test_user_logout()
    test_case.test_user_profile_get()
    test_case.test_user_profile_update()
    test_case.test_session_status()
    test_case.test_admin_create_user()
    test_case.test_user_roles_and_permissions()
    test_case.test_user_company_relationship()
    test_case.test_user_authentication_flow()
    
    print("\n" + "=" * 50)
    print("✅ TODAS LAS PRUEBAS DE USUARIOS COMPLETADAS")
    print("🎉 El sistema de usuarios está listo!")
