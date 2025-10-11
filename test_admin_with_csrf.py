#!/usr/bin/env python3
"""
Script para probar admin con manejo correcto de CSRF
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_admin_with_csrf():
    """Prueba admin con manejo de CSRF"""
    
    session = requests.Session()
    
    # 1. Obtener CSRF token
    print("1. Obteniendo CSRF token...")
    csrf_response = session.get(f"{BASE_URL}/user/test/")
    csrf_token = session.cookies.get('csrftoken')
    print(f"   CSRF Token: {csrf_token[:20]}..." if csrf_token else "   No CSRF token")
    
    # 2. Login como admin
    print("\n2. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data, headers=headers)
    
    if login_response.status_code != 200:
        print(f"ERROR - Login: {login_response.status_code}")
        return
    
    print("OK - Login exitoso")
    
    # 3. Listar diseñadores
    print("\n3. Listar diseñadores...")
    designers_response = session.get(f"{BASE_URL}/user/admin/designers/")
    if designers_response.status_code == 200:
        designers_data = designers_response.json()
        print(f"OK - Diseñadores: {designers_data['total']}")
        designers = designers_data['designers']
    else:
        print(f"ERROR - Diseñadores: {designers_response.status_code}")
        return
    
    # 4. Cambiar rol de usuario
    print("\n4. Cambiar rol de usuario...")
    
    # Obtener un cliente
    clients_response = session.get(f"{BASE_URL}/user/admin/users/?role=cliente")
    if clients_response.status_code == 200:
        clients_data = clients_response.json()
        if clients_data['users']:
            client = clients_data['users'][0]
            print(f"   Usuario: {client['username']} (ID: {client['id']})")
            
            # Cambiar a diseñador
            role_change_data = {
                "user_id": client['id'],
                "role": "diseñador"
            }
            
            headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
            role_response = session.post(f"{BASE_URL}/user/admin/set-role/", json=role_change_data, headers=headers)
            
            if role_response.status_code == 200:
                print("OK - Rol cambiado exitosamente")
            else:
                print(f"ERROR - Cambio de rol: {role_response.status_code}")
                print(f"   Response: {role_response.text}")
    
    # 5. Crear servicio
    print("\n5. Crear nuevo servicio...")
    
    # Obtener categorías
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    if categories_response.status_code == 200:
        categories = categories_response.json()
        if categories:
            category_id = categories[0]['id']
            
            service_data = {
                "name": "Servicio Admin Test",
                "description": "Servicio creado por admin",
                "service_type": "test",
                "base_price": 150,
                "features": ["Test feature 1", "Test feature 2"],
                "delivery_time": "3-5 días",
                "category": category_id
            }
            
            headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
            service_response = session.post(f"{BASE_URL}/branding/services/", json=service_data, headers=headers)
            
            if service_response.status_code == 201:
                service = service_response.json()
                print(f"OK - Servicio creado: {service['name']}")
            else:
                print(f"ERROR - Crear servicio: {service_response.status_code}")
                print(f"   Response: {service_response.text}")
    
    print("\nPrueba con CSRF completada!")

if __name__ == "__main__":
    test_admin_with_csrf()

