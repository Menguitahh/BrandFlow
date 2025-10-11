#!/usr/bin/env python3
"""
Script para probar el flujo completo de admin
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_admin_full_flow():
    """Prueba el flujo completo de admin"""
    
    session = requests.Session()
    
    # 1. Login como admin
    print("1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"ERROR - Login: {login_response.status_code}")
        return
    
    print("OK - Login exitoso")
    
    # 2. Listar diseñadores
    print("\n2. Listar diseñadores disponibles...")
    designers_response = session.get(f"{BASE_URL}/user/admin/designers/")
    
    if designers_response.status_code == 200:
        designers_data = designers_response.json()
        print(f"OK - Diseñadores: {designers_data['total']} disponibles")
        for designer in designers_data['designers']:
            print(f"   - {designer['username']} (ID: {designer['id']})")
    else:
        print(f"ERROR - Diseñadores: {designers_response.status_code}")
    
    # 3. Listar todos los usuarios con filtros
    print("\n3. Listar usuarios con filtros...")
    
    # Todos los usuarios
    all_users = session.get(f"{BASE_URL}/user/admin/users/")
    if all_users.status_code == 200:
        data = all_users.json()
        print(f"OK - Total usuarios: {data['total']}")
    
    # Solo diseñadores
    designers_only = session.get(f"{BASE_URL}/user/admin/users/?role=diseñador")
    if designers_only.status_code == 200:
        data = designers_only.json()
        print(f"OK - Solo diseñadores: {data['total']}")
    
    # Solo clientes
    clients_only = session.get(f"{BASE_URL}/user/admin/users/?role=cliente")
    if clients_only.status_code == 200:
        data = clients_only.json()
        print(f"OK - Solo clientes: {data['total']}")
    
    # 4. Cambiar rol de un usuario (crear un cliente y convertirlo en diseñador)
    print("\n4. Cambiar rol de usuario...")
    
    # Primero obtener un cliente
    clients_response = session.get(f"{BASE_URL}/user/admin/users/?role=cliente")
    if clients_response.status_code == 200:
        clients_data = clients_response.json()
        if clients_data['users']:
            client = clients_data['users'][0]
            print(f"   Usuario seleccionado: {client['username']} (ID: {client['id']})")
            
            # Cambiar a diseñador
            role_change_data = {
                "user_id": client['id'],
                "role": "diseñador"
            }
            
            role_response = session.post(f"{BASE_URL}/user/admin/set-role/", json=role_change_data)
            if role_response.status_code == 200:
                print(f"OK - Rol cambiado a diseñador")
            else:
                print(f"ERROR - Cambio de rol: {role_response.status_code}")
                print(f"   Response: {role_response.text}")
    
    # 5. Crear un nuevo servicio
    print("\n5. Crear nuevo servicio...")
    
    # Obtener categorías primero
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    if categories_response.status_code == 200:
        categories = categories_response.json()
        if categories:
            category_id = categories[0]['id']
            print(f"   Usando categoría: {categories[0]['name']} (ID: {category_id})")
            
            # Crear servicio
            service_data = {
                "name": "Servicio de Prueba Admin",
                "description": "Servicio creado por admin para testing",
                "service_type": "test",
                "base_price": 100,
                "features": ["Característica 1", "Característica 2"],
                "delivery_time": "2-3 días",
                "category": category_id
            }
            
            service_response = session.post(f"{BASE_URL}/branding/services/", json=service_data)
            if service_response.status_code == 201:
                service = service_response.json()
                print(f"OK - Servicio creado: {service['name']} (ID: {service['id']})")
            else:
                print(f"ERROR - Crear servicio: {service_response.status_code}")
                print(f"   Response: {service_response.text}")
    
    # 6. Listar servicios actualizados
    print("\n6. Listar servicios actualizados...")
    services_response = session.get(f"{BASE_URL}/branding/services/")
    if services_response.status_code == 200:
        services = services_response.json()
        print(f"OK - Total servicios: {len(services)}")
        for service in services[-3:]:  # Mostrar los últimos 3
            print(f"   - {service['name']} (${service['base_price']})")
    
    # 7. Probar asignación de diseñador (si hay proyectos)
    print("\n7. Probar asignación de diseñador...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"   Proyectos disponibles: {len(projects)}")
        
        if projects and designers_data['designers']:
            project = projects[0]
            designer = designers_data['designers'][0]
            
            print(f"   Asignando {designer['username']} al proyecto {project['title']}")
            
            assign_data = {"designer_id": designer['id']}
            assign_response = session.post(
                f"{BASE_URL}/branding/projects/{project['id']}/assign_designer/", 
                json=assign_data
            )
            
            if assign_response.status_code == 200:
                result = assign_response.json()
                print(f"OK - Diseñador asignado: {result['message']}")
            else:
                print(f"ERROR - Asignación: {assign_response.status_code}")
                print(f"   Response: {assign_response.text}")
        else:
            print("   No hay proyectos o diseñadores para asignar")
    
    print("\nPrueba completa finalizada!")

if __name__ == "__main__":
    test_admin_full_flow()

