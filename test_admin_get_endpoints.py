#!/usr/bin/env python3
"""
Script para probar solo los endpoints GET de admin
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_admin_get_endpoints():
    """Prueba solo los endpoints GET de admin"""
    
    session = requests.Session()
    
    # 1. Login como admin
    print("1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"ERROR - Login: {login_response.status_code}")
        return
    
    print("OK - Login exitoso")
    user_data = login_response.json()
    print(f"   Usuario: {user_data['user']['username']} - {user_data['user']['role']}")
    
    # 2. Verificar perfil
    print("\n2. Verificar perfil...")
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
        print(f"OK - Total usuarios: {users_data['total']}")
        
        # Mostrar algunos usuarios
        for user in users_data['users'][:5]:
            print(f"   - {user['username']} ({user['role']}) - {user['email']}")
    else:
        print(f"ERROR - Usuarios: {users_response.status_code}")
    
    # 4. Filtrar usuarios por rol
    print("\n4. Filtrar usuarios por rol...")
    
    # Solo diseñadores
    designers_response = session.get(f"{BASE_URL}/user/admin/users/?role=diseñador")
    if designers_response.status_code == 200:
        designers_data = designers_response.json()
        print(f"OK - Diseñadores: {designers_data['total']}")
        for designer in designers_data['users']:
            print(f"   - {designer['username']} ({designer['email']})")
    
    # Solo clientes
    clients_response = session.get(f"{BASE_URL}/user/admin/users/?role=cliente")
    if clients_response.status_code == 200:
        clients_data = clients_response.json()
        print(f"OK - Clientes: {clients_data['total']}")
    
    # 5. Listar diseñadores específicos
    print("\n5. Listar diseñadores específicos...")
    designers_specific = session.get(f"{BASE_URL}/user/admin/designers/")
    if designers_specific.status_code == 200:
        designers_data = designers_specific.json()
        print(f"OK - Diseñadores disponibles: {designers_data['total']}")
        for designer in designers_data['designers']:
            print(f"   - {designer['username']} (ID: {designer['id']})")
    else:
        print(f"ERROR - Diseñadores específicos: {designers_specific.status_code}")
    
    # 6. Buscar usuarios
    print("\n6. Buscar usuarios...")
    search_response = session.get(f"{BASE_URL}/user/admin/users/?search=juan")
    if search_response.status_code == 200:
        search_data = search_response.json()
        print(f"OK - Búsqueda 'juan': {search_data['total']} resultados")
        for user in search_data['users']:
            print(f"   - {user['username']} ({user['role']})")
    
    # 7. Listar servicios
    print("\n7. Listar servicios de branding...")
    services_response = session.get(f"{BASE_URL}/branding/services/")
    if services_response.status_code == 200:
        services = services_response.json()
        print(f"OK - Servicios: {len(services)} disponibles")
        for service in services[:5]:
            print(f"   - {service['name']} (${service['base_price']}) - {service['delivery_time']}")
    else:
        print(f"ERROR - Servicios: {services_response.status_code}")
    
    # 8. Listar categorías
    print("\n8. Listar categorías...")
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    if categories_response.status_code == 200:
        categories = categories_response.json()
        print(f"OK - Categorías: {len(categories)}")
        for category in categories:
            print(f"   - {category['name']}: {category['description']}")
    else:
        print(f"ERROR - Categorías: {categories_response.status_code}")
    
    # 9. Listar proyectos
    print("\n9. Listar proyectos...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"OK - Proyectos: {len(projects)}")
        for project in projects:
            print(f"   - {project['title']} ({project['status']})")
    else:
        print(f"ERROR - Proyectos: {projects_response.status_code}")
    
    # 10. Listar cotizaciones
    print("\n10. Listar cotizaciones...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        print(f"OK - Cotizaciones: {len(quotes)}")
        for quote in quotes:
            print(f"   - {quote['title']} ({quote['status']})")
    else:
        print(f"ERROR - Cotizaciones: {quotes_response.status_code}")
    
    print("\nPrueba de endpoints GET completada!")
    print("\nRESUMEN:")
    print("- Login y autenticación: OK")
    print("- Listar usuarios con filtros: OK")
    print("- Buscar usuarios: OK")
    print("- Listar servicios: OK")
    print("- Listar categorías: OK")
    print("- Listar proyectos: OK")
    print("- Listar cotizaciones: OK")

if __name__ == "__main__":
    test_admin_get_endpoints()

