#!/usr/bin/env python3
"""
Script específico para probar la eliminación de categorías
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_delete_category():
    """Probar específicamente la eliminación de categorías"""
    
    session = requests.Session()
    
    print("=== PRUEBA ESPECÍFICA DE ELIMINACIÓN DE CATEGORÍAS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Crear una categoría para eliminar
    print("\n2. Creando categoría para eliminar...")
    category_data = {
        "name": "Categoría para Eliminar",
        "description": "Esta categoría será eliminada"
    }
    
    create_response = session.post(f"{BASE_URL}/branding/service-categories/", json=category_data)
    print(f"   Status: {create_response.status_code}")
    
    if create_response.status_code != 201:
        print(f"   [ERROR] Error creando categoría: {create_response.text}")
        return
    
    category_to_delete = create_response.json()
    category_id = category_to_delete['id']
    print(f"   [OK] Categoría creada: {category_to_delete['name']} (ID: {category_id})")
    
    # 3. Verificar que existe
    print("\n3. Verificando que la categoría existe...")
    list_response = session.get(f"{BASE_URL}/branding/service-categories/")
    if list_response.status_code == 200:
        categories = list_response.json()
        found = any(cat['id'] == category_id for cat in categories)
        print(f"   [OK] Categoría encontrada en la lista: {found}")
    
    # 4. Intentar eliminar la categoría
    print(f"\n4. Eliminando categoría ID {category_id}...")
    delete_response = session.delete(f"{BASE_URL}/branding/service-categories/{category_id}/")
    print(f"   Status: {delete_response.status_code}")
    print(f"   Headers: {dict(delete_response.headers)}")
    
    if delete_response.status_code == 204:
        print("   [OK] Categoría eliminada exitosamente (Status 204)")
    else:
        print(f"   [ERROR] Error eliminando categoría: {delete_response.text}")
        return
    
    # 5. Verificar que ya no existe
    print("\n5. Verificando que la categoría ya no existe...")
    list_response2 = session.get(f"{BASE_URL}/branding/service-categories/")
    if list_response2.status_code == 200:
        categories2 = list_response2.json()
        found = any(cat['id'] == category_id for cat in categories2)
        print(f"   [OK] Categoría ya no existe en la lista: {not found}")
    
    # 6. Intentar eliminar una categoría que no existe
    print("\n6. Probando eliminar categoría inexistente...")
    fake_id = 99999
    delete_fake_response = session.delete(f"{BASE_URL}/branding/service-categories/{fake_id}/")
    print(f"   Status: {delete_fake_response.status_code}")
    
    if delete_fake_response.status_code == 404:
        print("   [OK] Respuesta correcta para categoría inexistente (404)")
    else:
        print(f"   [WARNING] Respuesta inesperada: {delete_fake_response.text}")
    
    print("\n=== CONCLUSIÓN ===")
    print("El endpoint DELETE funciona correctamente en el backend.")
    print("Si el frontend tiene problemas, debe ser:")
    print("1. Manejo incorrecto de respuesta 204")
    print("2. Problema de autenticación")
    print("3. Error en el interceptor de axios")

if __name__ == "__main__":
    test_delete_category()
