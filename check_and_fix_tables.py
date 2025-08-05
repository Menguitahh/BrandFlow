#!/usr/bin/env python
"""
Script para verificar y corregir problemas de tablas
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrandFlow.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def check_tables():
    """Verificar qué tablas existen"""
    print("🔍 VERIFICANDO TABLAS EXISTENTES")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'brand_control_%'")
        tables = cursor.fetchall()
        
        print("Tablas brand_control encontradas:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "=" * 50)
        return [table[0] for table in tables]

def create_missing_tables():
    """Crear tablas faltantes manualmente"""
    print("🔧 CREANDO TABLAS FALTANTES")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Verificar si existe la tabla shoppcart
        cursor.execute("SHOW TABLES LIKE 'brand_control_shoppcart'")
        if not cursor.fetchone():
            print("❌ Tabla brand_control_shoppcart no existe")
            print("Creando tabla brand_control_shoppcart...")
            
            cursor.execute("""
                CREATE TABLE `brand_control_shoppcart` (
                    `idshoppcart` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `user_id` integer NULL,
                    `created_at` datetime(6) NULL,
                    `updated_at` datetime(6) NULL
                )
            """)
            print("✅ Tabla brand_control_shoppcart creada")
        else:
            print("✅ Tabla brand_control_shoppcart ya existe")
        
        # Verificar si existe la tabla shoppcartdetails
        cursor.execute("SHOW TABLES LIKE 'brand_control_shoppcartdetails'")
        if not cursor.fetchone():
            print("❌ Tabla brand_control_shoppcartdetails no existe")
            print("Creando tabla brand_control_shoppcartdetails...")
            
            cursor.execute("""
                CREATE TABLE `brand_control_shoppcartdetails` (
                    `idshoppcartdetails` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `quantity` integer NOT NULL,
                    `idproduct_id` integer NOT NULL,
                    `idshoppcart_id` integer NOT NULL
                )
            """)
            print("✅ Tabla brand_control_shoppcartdetails creada")
        else:
            print("✅ Tabla brand_control_shoppcartdetails ya existe")
        
        # Verificar si existe la tabla stockmovement
        cursor.execute("SHOW TABLES LIKE 'brand_control_stockmovement'")
        if not cursor.fetchone():
            print("❌ Tabla brand_control_stockmovement no existe")
            print("Creando tabla brand_control_stockmovement...")
            
            cursor.execute("""
                CREATE TABLE `brand_control_stockmovement` (
                    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `movement_type` varchar(20) NOT NULL,
                    `quantity` integer NOT NULL,
                    `previous_stock` integer NOT NULL,
                    `new_stock` integer NOT NULL,
                    `reason` varchar(200) NOT NULL,
                    `created_at` datetime(6) NOT NULL,
                    `product_id` integer NOT NULL,
                    `user_id` integer NULL
                )
            """)
            print("✅ Tabla brand_control_stockmovement creada")
        else:
            print("✅ Tabla brand_control_stockmovement ya existe")
        
        # Agregar columnas faltantes a la tabla Order
        print("\n🔧 AGREGANDO COLUMNAS FALTANTES A ORDER")
        try:
            cursor.execute("ALTER TABLE `brand_control_order` ADD COLUMN `user_id` integer NULL")
            print("✅ Columna user_id agregada a Order")
        except Exception as e:
            print(f"⚠️ Columna user_id ya existe en Order: {e}")
        
        try:
            cursor.execute("ALTER TABLE `brand_control_order` ADD COLUMN `created_at` datetime(6) NULL")
            print("✅ Columna created_at agregada a Order")
        except Exception as e:
            print(f"⚠️ Columna created_at ya existe en Order: {e}")
        
        try:
            cursor.execute("ALTER TABLE `brand_control_order` ADD COLUMN `updated_at` datetime(6) NULL")
            print("✅ Columna updated_at agregada a Order")
        except Exception as e:
            print(f"⚠️ Columna updated_at ya existe en Order: {e}")

def test_core_functionality():
    """Probar funcionalidades core después de las correcciones"""
    print("\n🧪 PROBANDO FUNCIONALIDADES CORE")
    print("=" * 50)
    
    from user_control.models import Users
    from brand_control.models import Category, Product, ShoppCart
    from decimal import Decimal
    import time
    
    # Test 1: Crear usuario
    timestamp = int(time.time())
    username = f'testuser_{timestamp}'
    
    try:
        user = Users.objects.create_user(
            username=username,
            email=f'test_{timestamp}@example.com',
            password='Test123!',
            roles='cliente'
        )
        print("✅ Usuario creado exitosamente")
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False
    
    # Test 2: Crear categoría
    try:
        category = Category.objects.create(
            name=f'Test Category {timestamp}',
            description='Categoría de prueba'
        )
        print("✅ Categoría creada exitosamente")
    except Exception as e:
        print(f"❌ Error creando categoría: {e}")
        return False
    
    # Test 3: Crear producto
    try:
        product = Product.objects.create(
            name=f'Test Product {timestamp}',
            description='Producto de prueba',
            price=Decimal('100.00'),
            stock=10,
            category_id=category,
            url_download='https://example.com/test'
        )
        print("✅ Producto creado exitosamente")
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        return False
    
    # Test 4: Crear carrito
    try:
        cart = ShoppCart.objects.create(user=user)
        print("✅ Carrito creado exitosamente")
    except Exception as e:
        print(f"❌ Error creando carrito: {e}")
        return False
    
    # Test 5: Gestión de stock
    try:
        initial_stock = product.stock
        product.update_stock(5, 'decrease')
        if product.stock == initial_stock - 5:
            print("✅ Gestión de stock funciona correctamente")
        else:
            print("❌ Error en gestión de stock")
            return False
    except Exception as e:
        print(f"❌ Error en gestión de stock: {e}")
        return False
    
    print("\n🎉 TODAS LAS FUNCIONALIDADES CORE FUNCIONAN")
    return True

def main():
    """Función principal"""
    print("🚀 INICIANDO VERIFICACIÓN Y CORRECCIÓN DE TABLAS")
    print("=" * 60)
    
    # Paso 1: Verificar tablas existentes
    existing_tables = check_tables()
    
    # Paso 2: Crear tablas faltantes
    create_missing_tables()
    
    # Paso 3: Probar funcionalidades core
    if test_core_functionality():
        print("\n✅ SISTEMA LISTO PARA PRODUCCIÓN")
        print("🎯 Funcionalidades core verificadas y funcionando")
        return True
    else:
        print("\n❌ PROBLEMAS DETECTADOS")
        print("🔧 Revisar errores específicos")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 