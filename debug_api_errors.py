#!/usr/bin/env python
"""
Script para debuggear errores 500 en las APIs
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrandFlow.settings')
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user_control.models import Users
from brand_control.models import Category, Product, Order, ShoppCart
from decimal import Decimal
import time

def debug_product_creation():
    """Debuggear creación de productos"""
    print("\n=== DEBUG: CREACIÓN DE PRODUCTOS ===")
    
    client = APIClient()
    
    # Crear usuario admin
    timestamp = int(time.time())
    admin_user = Users.objects.create_user(
        username=f'admin_debug_{timestamp}',
        email=f'admin_debug_{timestamp}@example.com',
        password='Admin123!',
        roles='admin'
    )
    
    # Crear categoría
    category = Category.objects.create(
        name=f'Debug Category {timestamp}',
        description='Categoría para debug'
    )
    
    # Autenticar como admin
    client.force_authenticate(user=admin_user)
    
    # Datos del producto
    product_data = {
        'name': f'Debug Product {timestamp}',
        'description': 'Producto para debug',
        'price': '100.00',
        'stock': 10,
        'category_id': category.id,
        'url_download': 'https://example.com/debug'
    }
    
    print(f"Datos del producto: {product_data}")
    
    # Crear producto
    url = '/api/brand_control/model/Product/'
    response = client.post(url, product_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido de respuesta: {response.content}")
    
    if response.status_code == 500:
        print("❌ Error 500 en creación de productos")
        return False
    elif response.status_code == 201:
        print("✅ Creación de productos exitosa")
        return True
    else:
        print(f"❌ Error {response.status_code} en creación de productos")
        return False

def debug_order_creation():
    """Debuggear creación de pedidos"""
    print("\n=== DEBUG: CREACIÓN DE PEDIDOS ===")
    
    client = APIClient()
    
    # Crear usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'order_debug_{timestamp}',
        email=f'order_debug_{timestamp}@example.com',
        password='Order123!',
        roles='cliente'
    )
    
    # Autenticar usuario
    client.force_authenticate(user=user)
    
    # Crear pedido
    order_data = {
        'user': user.id,
        'status': 'pending',
        'total': '60.00'
    }
    
    print(f"Datos del pedido: {order_data}")
    
    url = '/api/brand_control/model/Order/'
    response = client.post(url, order_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido de respuesta: {response.content}")
    
    if response.status_code == 500:
        print("❌ Error 500 en creación de pedidos")
        return False
    elif response.status_code == 201:
        print("✅ Creación de pedidos exitosa")
        return True
    else:
        print(f"❌ Error {response.status_code} en creación de pedidos")
        return False

def debug_cart_operations():
    """Debuggear operaciones de carrito"""
    print("\n=== DEBUG: OPERACIONES DE CARRITO ===")
    
    client = APIClient()
    
    # Crear usuario
    timestamp = int(time.time())
    user = Users.objects.create_user(
        username=f'cart_debug_{timestamp}',
        email=f'cart_debug_{timestamp}@example.com',
        password='Cart123!',
        roles='cliente'
    )
    
    # Crear producto
    category = Category.objects.create(
        name=f'Cart Debug Category {timestamp}',
        description='Categoría para debug de carrito'
    )
    
    product = Product.objects.create(
        name=f'Cart Debug Product {timestamp}',
        description='Producto para debug de carrito',
        price=Decimal('25.00'),
        stock=15,
        category_id=category,
        url_download='https://example.com/cart-debug'
    )
    
    # Crear carrito
    cart = ShoppCart.objects.create(user=user)
    
    # Autenticar usuario
    client.force_authenticate(user=user)
    
    # Agregar producto al carrito
    cart_detail_data = {
        'idproduct': product.id,
        'idshoppcart': cart.idshoppcart,
        'quantity': 2
    }
    
    print(f"Datos del carrito: {cart_detail_data}")
    
    url = '/api/brand_control/model/shoppcartdetails/'
    response = client.post(url, cart_detail_data, format='json')
    
    print(f"Código de respuesta: {response.status_code}")
    print(f"Contenido de respuesta: {response.content}")
    
    if response.status_code == 500:
        print("❌ Error 500 en operaciones de carrito")
        return False
    elif response.status_code == 201:
        print("✅ Operaciones de carrito exitosas")
        return True
    else:
        print(f"❌ Error {response.status_code} en operaciones de carrito")
        return False

def main():
    """Función principal"""
    print("🔍 DEBUGGEANDO ERRORES 500")
    print("=" * 50)
    
    tests = [
        ("Creación de productos", debug_product_creation),
        ("Creación de pedidos", debug_order_creation),
        ("Operaciones de carrito", debug_cart_operations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} falló")
        except Exception as e:
            print(f"❌ {test_name} falló con error: {str(e)}")
    
    print(f"\nRESULTADOS: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 TODOS LOS ERRORES 500 CORREGIDOS")
    else:
        print("⚠️ Algunos errores 500 persisten")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 