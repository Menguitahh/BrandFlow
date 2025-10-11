#!/usr/bin/env python
"""
Script específico para probar registro de usuarios y creación de pedidos
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


class RegistrationTests(TestCase):
    def setUp(self):
        self.api = APIClient()

    def test_register_default_role_client(self):
        r = self.api.post('/api/user/register/', {
            'username': 'c1', 'email': 'c1@example.com', 'password': 'Test123!', 'password2': 'Test123!', 'roles': 'admin'
        }, format='json')
        self.assertEqual(r.status_code, 201)
        u = Users.objects.get(username='c1')
        self.assertEqual(u.roles, 'cliente')
from rest_framework.test import APIClient
from rest_framework import status
from user_control.models import Users
from brand_control.models import Category, Product, Order, ShoppCart
from decimal import Decimal
import time

def test_user_registration_direct():
    """Probar registro de usuarios de forma directa"""
    print("\n=== PRUEBA DIRECTA: REGISTRO DE USUARIOS ===")
    
    client = APIClient()
    
    # Usar timestamp único para evitar duplicados
    timestamp = int(time.time())
    username = f'testuser_direct_{timestamp}'
    
    # Datos del usuario
    user_data = {
        'username': username,
        'email': f'test_direct_{timestamp}@example.com',
        'password': 'Test123!',
        'password2': 'Test123!',
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '123456789',
        'address': 'Calle Test 123',
        'roles': 'cliente'
    }
    
    print(f"Intentando registrar usuario: {username}")
    print(f"Datos: {user_data}")
    
    # Realizar registro
    url = '/api/user/register/'
    response = client.post(url, user_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido de respuesta: {response.data}")
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Registro de usuario exitoso")
        return True
    elif response.status_code == status.HTTP_400_BAD_REQUEST:
        print("❌ Error en registro (400)")
        print(f"Detalles: {response.data}")
        return False
    else:
        print(f"❌ Error inesperado: {response.status_code}")
        return False

def test_order_creation_direct():
    """Probar creación de pedidos de forma directa"""
    print("\n=== PRUEBA DIRECTA: CREACIÓN DE PEDIDOS ===")
    
    client = APIClient()
    
    # Crear usuario directamente en la base de datos
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'orderuser_direct_{timestamp}',
        email=f'order_direct_{timestamp}@example.com',
        password='Order123!',
        first_name='Order',
        last_name='User',
        roles='cliente'
    )
    
    print(f"Usuario creado: {user.username}")
    
    # Autenticar usuario
    client.force_authenticate(user=user)
    
    # Crear pedido directamente
    try:
        order = Order.objects.create(
            user=user,
            status='pending',
            total=Decimal('60.00')
        )
        print(f"✅ Pedido creado directamente: ID {order.idorder}")
        print(f"   Usuario: {order.user.username}")
        print(f"   Estado: {order.status}")
        print(f"   Total: {order.total}")
        return True
    except Exception as e:
        print(f"❌ Error creando pedido directamente: {e}")
        return False

def test_order_creation_via_api():
    """Probar creación de pedidos vía API"""
    print("\n=== PRUEBA DIRECTA: CREACIÓN DE PEDIDOS VÍA API ===")
    
    client = APIClient()
    
    # Crear usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'orderuser_api_{timestamp}',
        email=f'order_api_{timestamp}@example.com',
        password='Order123!',
        first_name='Order',
        last_name='User',
        roles='cliente'
    )
    
    print(f"Usuario creado: {user.username}")
    
    # Autenticar usuario
    client.force_authenticate(user=user)
    
    # Datos del pedido
    order_data = {
        'user': user.id,
        'status': 'pending',
        'total': '75.00'
    }
    
    print(f"Datos del pedido: {order_data}")
    
    # Crear pedido vía API
    url = '/api/brand_control/model/Order/'
    response = client.post(url, order_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido de respuesta: {response.data}")
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Creación de pedido vía API exitosa")
        return True
    else:
        print(f"❌ Error en creación de pedido vía API: {response.status_code}")
        return False

def test_complete_flow():
    """Probar flujo completo: registro -> login -> crear pedido"""
    print("\n=== PRUEBA DIRECTA: FLUJO COMPLETO ===")
    
    client = APIClient()
    
    # Paso 1: Crear usuario
    timestamp = int(time.time())
    username = f'flowuser_{timestamp}'
    
    user = Users.objects.create_user(
        username=username,
        email=f'flow_{timestamp}@example.com',
        password='Flow123!',
        first_name='Flow',
        last_name='User',
        roles='cliente'
    )
    
    print(f"✅ Usuario creado: {user.username}")
    
    # Paso 2: Login
    login_data = {
        'identifier': username,
        'password': 'Flow123!'
    }
    
    url = '/api/user/login/'
    response = client.post(url, login_data, format='json')
    
    if response.status_code == status.HTTP_200_OK:
        print("✅ Login exitoso")
        session_id = response.data.get('session_id')
        print(f"   Session ID: {session_id}")
    else:
        print(f"❌ Error en login: {response.status_code}")
        return False
    
    # Paso 3: Crear pedido autenticado
    client.force_authenticate(user=user)
    
    order_data = {
        'user': user.id,
        'status': 'pending',
        'total': '100.00'
    }
    
    url = '/api/brand_control/model/Order/'
    response = client.post(url, order_data, format='json')
    
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Pedido creado exitosamente")
        print(f"   Pedido ID: {response.data.get('idorder')}")
        print(f"   Total: {response.data.get('total')}")
        return True
    else:
        print(f"❌ Error creando pedido: {response.status_code}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBAS DIRECTAS DE REGISTRO Y PEDIDOS")
    print("=" * 60)
    
    tests = [
        ("Registro de usuarios", test_user_registration_direct),
        ("Creación de pedidos directa", test_order_creation_direct),
        ("Creación de pedidos vía API", test_order_creation_via_api),
        ("Flujo completo", test_complete_flow),
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
        print("🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ El sistema está funcionando correctamente")
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("🔧 Revisar errores específicos")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 