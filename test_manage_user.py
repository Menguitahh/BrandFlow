#!/usr/bin/env python
"""
Script para probar todas las funcionalidades de gestión de usuarios (manage_user)
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrandFlow.settings')
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from user_control.models import Users


class RoleChangeTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.admin = Users.objects.create_user(username='admin', email='a@example.com', password='Admin123!', roles='admin')
        self.user = Users.objects.create_user(username='u', email='u@example.com', password='Test123!', roles='cliente')

    def test_admin_set_role(self):
        self.api.force_authenticate(user=self.admin)
        r = self.api.post('/api/user/admin/set-role/', {'user_id': self.user.id, 'role': 'diseñador'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.roles, 'diseñador')
from rest_framework.test import APIClient
from rest_framework import status
from user_control.models import Users
from brand_control.models import Branch
from decimal import Decimal
import time

def test_user_registration():
    """Probar registro de usuarios"""
    print("\n=== PRUEBA: REGISTRO DE USUARIOS ===")
    
    client = APIClient()
    
    timestamp = int(time.time())
    username = f'testuser_manage_{timestamp}'
    
    user_data = {
        'username': username,
        'email': f'test_manage_{timestamp}@example.com',
        'password': 'Test123!',
        'password2': 'Test123!',
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '123456789',
        'address': 'Calle Test 123',
        'roles': 'cliente'
    }
    
    url = '/api/user/register/'
    response = client.post(url, user_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido: {response.data}")
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Registro de usuarios funcionando")
        return True
    else:
        print("❌ Error en registro de usuarios")
        return False

def test_user_login():
    """Probar login de usuarios"""
    print("\n=== PRUEBA: LOGIN DE USUARIOS ===")
    
    client = APIClient()
    
    # Crear usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'loginuser_{timestamp}',
        email=f'login_{timestamp}@example.com',
        password='Login123!',
        first_name='Login',
        last_name='User',
        roles='cliente'
    )
    
    # Probar login por username
    login_data = {
        'identifier': user.username,
        'password': 'Login123!'
    }
    
    url = '/api/user/login/'
    response = client.post(url, login_data, format='json')
    
    print(f"Login por username - Código: {response.status_code}")
    
    if response.status_code == status.HTTP_200_OK:
        print("✅ Login por username funcionando")
        
        # Probar login por email
        login_data_email = {
            'identifier': user.email,
            'password': 'Login123!'
        }
        
        response_email = client.post(url, login_data_email, format='json')
        print(f"Login por email - Código: {response_email.status_code}")
        
        if response_email.status_code == status.HTTP_200_OK:
            print("✅ Login por email funcionando")
            return True
        else:
            print("❌ Error en login por email")
            return False
    else:
        print("❌ Error en login por username")
        return False

def test_user_logout():
    """Probar logout de usuarios"""
    print("\n=== PRUEBA: LOGOUT DE USUARIOS ===")
    
    client = APIClient()
    
    # Crear y autenticar usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'logoutuser_{timestamp}',
        email=f'logout_{timestamp}@example.com',
        password='Logout123!',
        roles='cliente'
    )
    
    client.force_authenticate(user=user)
    
    # Probar logout
    url = '/api/user/logout/'
    response = client.post(url)
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido: {response.data}")
    
    if response.status_code == status.HTTP_200_OK:
        print("✅ Logout funcionando")
        return True
    else:
        print("❌ Error en logout")
        return False

def test_user_profile():
    """Probar gestión de perfil de usuario"""
    print("\n=== PRUEBA: GESTIÓN DE PERFIL ===")
    
    client = APIClient()
    
    # Crear y autenticar usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'profileuser_{timestamp}',
        email=f'profile_{timestamp}@example.com',
        password='Profile123!',
        first_name='Profile',
        last_name='User',
        phone='987654321',
        address='Calle Profile 456',
        roles='cliente'
    )
    
    client.force_authenticate(user=user)
    
    # Probar GET profile
    url = '/api/user/profile/'
    response = client.get(url)
    
    print(f"GET Profile - Código: {response.status_code}")
    print(f"Datos del perfil: {response.data}")
    
    if response.status_code == status.HTTP_200_OK:
        print("✅ GET Profile funcionando")
        
        # Probar PUT profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Profile',
            'phone': '111222333',
            'address': 'Nueva Dirección 789'
        }
        
        response_put = client.put(url, update_data, format='json')
        print(f"PUT Profile - Código: {response_put.status_code}")
        
        if response_put.status_code == status.HTTP_200_OK:
            print("✅ PUT Profile funcionando")
            return True
        else:
            print("❌ Error en PUT Profile")
            return False
    else:
        print("❌ Error en GET Profile")
        return False

def test_session_status():
    """Probar verificación de estado de sesión"""
    print("\n=== PRUEBA: ESTADO DE SESIÓN ===")
    
    client = APIClient()
    
    # Probar sin autenticación
    url = '/api/user/session-status/'
    response = client.get(url)
    
    print(f"Sin autenticación - Código: {response.status_code}")
    print(f"Contenido: {response.data}")
    
    if response.status_code == status.HTTP_200_OK and not response.data.get('authenticated'):
        print("✅ Estado de sesión sin autenticación funcionando")
        
        # Crear y autenticar usuario
        timestamp = int(time.time())
        user = Users.objects.create_user(
            username=f'sessionuser_{timestamp}',
            email=f'session_{timestamp}@example.com',
            password='Session123!',
            roles='cliente'
        )
        
        client.force_authenticate(user=user)
        
        # Probar con autenticación
        response_auth = client.get(url)
        print(f"Con autenticación - Código: {response_auth.status_code}")
        
        if response_auth.status_code == status.HTTP_200_OK and response_auth.data.get('authenticated'):
            print("✅ Estado de sesión con autenticación funcionando")
            return True
        else:
            print("❌ Error en estado de sesión con autenticación")
            return False
    else:
        print("❌ Error en estado de sesión sin autenticación")
        return False

def test_admin_create_user():
    """Probar creación de usuarios por admin"""
    print("\n=== PRUEBA: CREACIÓN DE USUARIOS POR ADMIN ===")
    
    client = APIClient()
    
    # Crear admin
    timestamp = int(time.time())
    admin = Users.objects.create_user(
        username=f'admin_{timestamp}',
        email=f'admin_{timestamp}@example.com',
        password='Admin123!',
        first_name='Admin',
        last_name='User',
        roles='admin'
    )
    
    client.force_authenticate(user=admin)
    
    # Crear usuario por admin
    new_user_data = {
        'username': f'newuser_{timestamp}',
        'email': f'newuser_{timestamp}@example.com',
        'password': 'NewUser123!',
        'password2': 'NewUser123!',
        'first_name': 'New',
        'last_name': 'User',
        'phone': '555666777',
        'address': 'Calle Nueva 123',
        'roles': 'cliente'
    }
    
    url = '/api/user/admin/create-user/'
    response = client.post(url, new_user_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido: {response.data}")
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Creación de usuarios por admin funcionando")
        return True
    else:
        print("❌ Error en creación de usuarios por admin")
        return False

def test_admin_create_branch():
    """Probar creación de sucursales por admin"""
    print("\n=== PRUEBA: CREACIÓN DE SUCURSALES POR ADMIN ===")
    
    client = APIClient()
    
    # Crear admin
    timestamp = int(time.time())
    admin = Users.objects.create_user(
        username=f'admin_branch_{timestamp}',
        email=f'admin_branch_{timestamp}@example.com',
        password='Admin123!',
        first_name='Admin',
        last_name='Branch',
        roles='admin'
    )
    
    client.force_authenticate(user=admin)
    
    # Crear sucursal por admin
    branch_data = {
        'name': f'Sucursal Test {timestamp}',
        'address': 'Calle Sucursal 456',
        'phone': '888999000'
    }
    
    url = '/api/user/admin/create-branch/'
    response = client.post(url, branch_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido: {response.data}")
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Creación de sucursales por admin funcionando")
        return True
    else:
        print("❌ Error en creación de sucursales por admin")
        return False

def test_protected_view():
    """Probar vista protegida"""
    print("\n=== PRUEBA: VISTA PROTEGIDA ===")
    
    client = APIClient()
    
    # Probar sin autenticación
    url = '/api/user/protected/'
    response = client.get(url)
    
    print(f"Sin autenticación - Código: {response.status_code}")
    
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        print("✅ Vista protegida sin autenticación funcionando")
        
        # Crear y autenticar usuario
        timestamp = int(time.time())
        user = Users.objects.create_user(
            username=f'protecteduser_{timestamp}',
            email=f'protected_{timestamp}@example.com',
            password='Protected123!',
            roles='cliente'
        )
        
        client.force_authenticate(user=user)
        
        # Probar con autenticación
        response_auth = client.get(url)
        print(f"Con autenticación - Código: {response_auth.status_code}")
        
        if response_auth.status_code == status.HTTP_200_OK:
            print("✅ Vista protegida con autenticación funcionando")
            return True
        else:
            print("❌ Error en vista protegida con autenticación")
            return False
    else:
        print("❌ Error en vista protegida sin autenticación")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBAS DE GESTIÓN DE USUARIOS (MANAGE_USER)")
    print("=" * 60)
    
    tests = [
        ("Registro de usuarios", test_user_registration),
        ("Login de usuarios", test_user_login),
        ("Logout de usuarios", test_user_logout),
        ("Gestión de perfil", test_user_profile),
        ("Estado de sesión", test_session_status),
        ("Creación de usuarios por admin", test_admin_create_user),
        ("Creación de sucursales por admin", test_admin_create_branch),
        ("Vista protegida", test_protected_view),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - EXITOSO")
            else:
                print(f"❌ {test_name} - FALLÓ")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"RESULTADOS: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 TODAS LAS PRUEBAS DE GESTIÓN DE USUARIOS PASARON")
        print("✅ El sistema de gestión de usuarios está funcionando correctamente")
    else:
        print("⚠️ Algunas pruebas de gestión de usuarios fallaron")
        print("🔧 Revisar errores específicos")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 