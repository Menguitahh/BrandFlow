#!/usr/bin/env python3
"""
Script para probar todos los endpoints de admin
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_admin_endpoints():
    """Prueba todos los endpoints de admin"""
    
    # 1. Login como admin
    print("1. Login como admin...")
    login_data = {
        "identifier": "admin",
        "password": "Admin123!"
    }
    
    session = requests.Session()
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code == 200:
        print("OK - Login exitoso")
        user_data = login_response.json()
        print(f"   Usuario: {user_data['user']['username']}")
        print(f"   Rol: {user_data['user']['role']}")
    else:
        print(f"ERROR - Login: {login_response.status_code}")
        return
    
    # 2. Verificar perfil de admin
    print("\n2. Verificar perfil de admin...")
    profile_response = session.get(f"{BASE_URL}/user/profile/")
    
    if profile_response.status_code == 200:
        profile = profile_response.json()
        print(f"OK - Perfil: {profile['username']} - {profile['role']}")
    else:
        print(f"ERROR - Perfil: {profile_response.status_code}")
    
    # 3. Listar todos los usuarios
    print("\n3. Listar todos los usuarios...")
    users_response = session.get(f"{BASE_URL}/user/admin/users/")
    
    if users_response.status_code == 200:
        users_data = users_response.json()
        print(f"OK - Usuarios: {users_data['total']} usuarios")
        for user in users_data['users'][:3]:  # Mostrar solo los primeros 3
            print(f"   - {user['username']} ({user['role']})")
    else:
        print(f"ERROR - Usuarios: {users_response.status_code}")
    
    # 4. Filtrar usuarios por rol
    print("\n4. Filtrar usuarios por rol 'cliente'...")
    filter_response = session.get(f"{BASE_URL}/user/admin/users/?role=cliente")
    
    if filter_response.status_code == 200:
        filter_data = filter_response.json()
        print(f"OK - Filtro: {filter_data['total']} clientes")
    else:
        print(f"ERROR - Filtro: {filter_response.status_code}")
    
    # 5. Listar diseñadores
    print("\n5. Listar diseñadores...")
    designers_response = session.get(f"{BASE_URL}/user/admin/designers/")
    
    if designers_response.status_code == 200:
        designers_data = designers_response.json()
        print(f"OK - Diseñadores: {designers_data['total']} diseñadores")
        for designer in designers_data['designers']:
            print(f"   - {designer['username']} ({designer['email']})")
    else:
        print(f"ERROR - Diseñadores: {designers_response.status_code}")
    
    # 6. Listar servicios
    print("\n6. Listar servicios de branding...")
    services_response = session.get(f"{BASE_URL}/branding/services/")
    
    if services_response.status_code == 200:
        services = services_response.json()
        print(f"OK - Servicios: {len(services)} servicios disponibles")
        for service in services[:3]:  # Mostrar solo los primeros 3
            print(f"   - {service['name']} (${service['base_price']})")
    else:
        print(f"ERROR - Servicios: {services_response.status_code}")
    
    # 7. Listar categorías de servicios
    print("\n7. Listar categorías de servicios...")
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    
    if categories_response.status_code == 200:
        categories = categories_response.json()
        print(f"OK - Categorías: {len(categories)} categorías")
        for category in categories:
            print(f"   - {category['name']}")
    else:
        print(f"ERROR - Categorías: {categories_response.status_code}")
    
    # 8. Listar proyectos
    print("\n8. Listar proyectos...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"OK - Proyectos: {len(projects)} proyectos")
        for project in projects[:3]:  # Mostrar solo los primeros 3
            print(f"   - {project['title']} ({project['status']})")
    else:
        print(f"ERROR - Proyectos: {projects_response.status_code}")
    
    # 9. Listar cotizaciones
    print("\n9. Listar cotizaciones...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        print(f"OK - Cotizaciones: {len(quotes)} cotizaciones")
        for quote in quotes[:3]:  # Mostrar solo los primeros 3
            print(f"   - {quote['title']} ({quote['status']})")
    else:
        print(f"ERROR - Cotizaciones: {quotes_response.status_code}")
    
    print("\nPrueba de endpoints completada!")

if __name__ == "__main__":
    test_admin_endpoints()
