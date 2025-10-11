#!/usr/bin/env python3
"""
Script para diagnosticar problemas de autenticación
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_auth_issue():
    """Diagnosticar problemas de autenticación"""
    
    session = requests.Session()
    
    print("=== DIAGNÓSTICO DE AUTENTICACIÓN ===")
    
    # 1. Login como admin
    print("\n1. Intentando login como admin...")
    login_data = {
        "identifier": "admin",
        "password": "Admin123!"
    }
    
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    print(f"   Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("   [OK] Login exitoso")
        user_data = login_response.json()
        print(f"   Usuario: {user_data['user']['username']}")
        print(f"   Rol: {user_data['user']['role']}")
    else:
        print(f"   [ERROR] Error en login: {login_response.text}")
        return
    
    # 2. Verificar perfil
    print("\n2. Verificando perfil...")
    profile_response = session.get(f"{BASE_URL}/user/profile/")
    print(f"   Status: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        profile = profile_response.json()
        print(f"   [OK] Perfil: {profile['username']} - {profile['role']}")
    else:
        print(f"   [ERROR] Error en perfil: {profile_response.text}")
        return
    
    # 3. Probar crear servicio
    print("\n3. Probando crear servicio...")
    
    # Obtener categorías primero
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    if categories_response.status_code == 200:
        categories = categories_response.json()
        if categories:
            category_id = categories[0]['id']
            print(f"   Usando categoría: {categories[0]['name']} (ID: {category_id})")
            
            # Intentar crear servicio
            service_data = {
                "name": "Servicio de Prueba",
                "description": "Descripción de prueba",
                "service_type": "test",
                "base_price": 100,
                "features": ["Feature 1", "Feature 2"],
                "delivery_time": "2-3 días",
                "category_id": category_id
            }
            
            service_response = session.post(f"{BASE_URL}/branding/services/", json=service_data)
            print(f"   Status: {service_response.status_code}")
            
            if service_response.status_code == 201:
                print("   [OK] Servicio creado exitosamente")
                service = service_response.json()
                print(f"   ID: {service['id']}, Nombre: {service['name']}")
            else:
                print(f"   [ERROR] Error creando servicio: {service_response.text}")
        else:
            print("   [ERROR] No hay categorías disponibles")
    else:
        print(f"   [ERROR] Error obteniendo categorías: {categories_response.status_code}")
    
    # 4. Probar crear categoría
    print("\n4. Probando crear categoría...")
    category_data = {
        "name": "Categoría de Prueba",
        "description": "Descripción de categoría de prueba"
    }
    
    category_response = session.post(f"{BASE_URL}/branding/service-categories/", json=category_data)
    print(f"   Status: {category_response.status_code}")
    
    if category_response.status_code == 201:
        print("   [OK] Categoría creada exitosamente")
        category = category_response.json()
        print(f"   ID: {category['id']}, Nombre: {category['name']}")
    else:
        print(f"   [ERROR] Error creando categoría: {category_response.text}")
    
    # 5. Probar cambiar rol de usuario
    print("\n5. Probando cambiar rol de usuario...")
    
    # Obtener un usuario
    users_response = session.get(f"{BASE_URL}/user/admin/users/")
    if users_response.status_code == 200:
        users_data = users_response.json()
        if users_data['users']:
            user = users_data['users'][0]
            print(f"   Usuario seleccionado: {user['username']} (ID: {user['id']})")
            
            role_data = {
                "user_id": user['id'],
                "role": "diseñador"
            }
            
            role_response = session.post(f"{BASE_URL}/user/admin/set-role/", json=role_data)
            print(f"   Status: {role_response.status_code}")
            
            if role_response.status_code == 200:
                print("   [OK] Rol cambiado exitosamente")
            else:
                print(f"   [ERROR] Error cambiando rol: {role_response.text}")
        else:
            print("   [ERROR] No hay usuarios disponibles")
    else:
        print(f"   [ERROR] Error obteniendo usuarios: {users_response.status_code}")
    
    print("\n=== DIAGNÓSTICO COMPLETADO ===")

if __name__ == "__main__":
    test_auth_issue()
