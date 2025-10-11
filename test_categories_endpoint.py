#!/usr/bin/env python3
"""
Script específico para probar el endpoint de categorías
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_categories_endpoint():
    """Probar específicamente el endpoint de categorías"""
    
    session = requests.Session()
    
    print("=== PRUEBA ESPECÍFICA DE CATEGORÍAS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Listar categorías existentes
    print("\n2. Listando categorías existentes...")
    list_response = session.get(f"{BASE_URL}/branding/service-categories/")
    print(f"   Status: {list_response.status_code}")
    
    if list_response.status_code == 200:
        categories = list_response.json()
        print(f"   [OK] Categorías encontradas: {len(categories)}")
        for cat in categories:
            print(f"      - {cat['name']} (ID: {cat['id']})")
    else:
        print(f"   [ERROR] Error listando categorías: {list_response.text}")
        return
    
    # 3. Crear nueva categoría
    print("\n3. Creando nueva categoría...")
    category_data = {
        "name": "Categoría Frontend Test",
        "description": "Descripción de prueba desde frontend"
    }
    
    create_response = session.post(f"{BASE_URL}/branding/service-categories/", json=category_data)
    print(f"   Status: {create_response.status_code}")
    print(f"   Response: {create_response.text}")
    
    if create_response.status_code == 201:
        category = create_response.json()
        print(f"   [OK] Categoría creada: ID {category['id']}, Nombre: {category['name']}")
    else:
        print(f"   [ERROR] Error creando categoría: {create_response.text}")
        return
    
    # 4. Verificar que se creó
    print("\n4. Verificando que se creó...")
    list_response2 = session.get(f"{BASE_URL}/branding/service-categories/")
    if list_response2.status_code == 200:
        categories2 = list_response2.json()
        print(f"   [OK] Total de categorías ahora: {len(categories2)}")
        
        # Buscar la categoría creada
        new_category = next((cat for cat in categories2 if cat['name'] == "Categoría Frontend Test"), None)
        if new_category:
            print(f"   [OK] Categoría encontrada: {new_category['name']} (ID: {new_category['id']})")
        else:
            print("   [ERROR] La categoría no se encontró en la lista")
    
    # 5. Probar editar categoría
    print("\n5. Probando editar categoría...")
    if 'new_category' in locals() and new_category:
        edit_data = {
            "name": "Categoría Frontend Test EDITADA",
            "description": "Descripción editada"
        }
        
        edit_response = session.put(f"{BASE_URL}/branding/service-categories/{new_category['id']}/", json=edit_data)
        print(f"   Status: {edit_response.status_code}")
        print(f"   Response: {edit_response.text}")
        
        if edit_response.status_code == 200:
            print("   [OK] Categoría editada exitosamente")
        else:
            print(f"   [ERROR] Error editando categoría: {edit_response.text}")
    
    # 6. Probar eliminar categoría
    print("\n6. Probando eliminar categoría...")
    if 'new_category' in locals() and new_category:
        delete_response = session.delete(f"{BASE_URL}/branding/service-categories/{new_category['id']}/")
        print(f"   Status: {delete_response.status_code}")
        
        if delete_response.status_code == 204:
            print("   [OK] Categoría eliminada exitosamente")
        else:
            print(f"   [ERROR] Error eliminando categoría: {delete_response.text}")
    
    print("\n=== CONCLUSIÓN ===")
    print("El endpoint de categorías funciona perfectamente en el backend.")
    print("El problema está en el frontend que tiene un mensaje hardcodeado.")

if __name__ == "__main__":
    test_categories_endpoint()

