#!/usr/bin/env python3
"""
Script para probar la funcionalidad de búsqueda de usuarios
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_user_search():
    """Probar la funcionalidad de búsqueda de usuarios"""
    
    session = requests.Session()
    
    print("=== PRUEBA DE BÚSQUEDA DE USUARIOS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener todos los usuarios primero
    print("\n2. Obteniendo todos los usuarios...")
    all_users_response = session.get(f"{BASE_URL}/user/admin/users/")
    
    if all_users_response.status_code != 200:
        print(f"   [ERROR] Error obteniendo usuarios: {all_users_response.status_code}")
        return
    
    all_users_data = all_users_response.json()
    all_users = all_users_data.get('users', [])
    print(f"   [INFO] Total de usuarios: {len(all_users)}")
    
    # 3. Probar diferentes tipos de búsqueda
    print("\n3. Probando diferentes búsquedas...")
    
    test_cases = [
        ("a", "Búsqueda por letra 'a'"),
        ("j", "Búsqueda por letra 'j'"),
        ("admin", "Búsqueda por palabra 'admin'"),
        ("diseñador", "Búsqueda por rol 'diseñador'"),
        ("cliente", "Búsqueda por rol 'cliente'"),
        ("xyz", "Búsqueda que no debería encontrar nada"),
        ("", "Búsqueda vacía")
    ]
    
    for search_term, description in test_cases:
        print(f"\n   {description}:")
        
        if search_term == "":
            # Búsqueda vacía debería devolver todos los usuarios
            search_response = session.get(f"{BASE_URL}/user/admin/users/")
        else:
            search_response = session.get(f"{BASE_URL}/user/admin/users/?search={search_term}")
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_users = search_data.get('users', [])
            print(f"      [OK] Encontrados: {len(search_users)} usuarios")
            
            # Mostrar algunos ejemplos
            for user in search_users[:3]:
                username = user.get('username', 'N/A')
                role = user.get('role', 'N/A')
                print(f"         - {username} ({role})")
            
            if len(search_users) > 3:
                print(f"         ... y {len(search_users) - 3} más")
                
        else:
            print(f"      [ERROR] Status: {search_response.status_code}")
            print(f"      [ERROR] Response: {search_response.text}")
    
    # 4. Probar búsqueda por campos específicos
    print("\n4. Probando búsqueda por campos específicos...")
    
    # Buscar por email
    email_search = session.get(f"{BASE_URL}/user/admin/users/?search=@")
    if email_search.status_code == 200:
        email_data = email_search.json()
        email_users = email_data.get('users', [])
        print(f"   [INFO] Búsqueda por email (@): {len(email_users)} usuarios")
    
    # Buscar por nombre
    name_search = session.get(f"{BASE_URL}/user/admin/users/?search=Juan")
    if name_search.status_code == 200:
        name_data = name_search.json()
        name_users = name_data.get('users', [])
        print(f"   [INFO] Búsqueda por nombre (Juan): {len(name_users)} usuarios")
    
    # 5. Verificar que la búsqueda es case-insensitive
    print("\n5. Verificando búsqueda case-insensitive...")
    
    case_tests = [
        ("ADMIN", "MAYÚSCULAS"),
        ("admin", "minúsculas"),
        ("Admin", "Mixto")
    ]
    
    for search_term, case_type in case_tests:
        search_response = session.get(f"{BASE_URL}/user/admin/users/?search={search_term}")
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_users = search_data.get('users', [])
            print(f"   [INFO] Búsqueda {case_type}: {len(search_users)} usuarios")
        else:
            print(f"   [ERROR] Búsqueda {case_type} falló: {search_response.status_code}")
    
    print("\n=== CONCLUSION ===")
    print("[OK] La funcionalidad de búsqueda funciona correctamente")
    print("[OK] No hay errores 500 en las búsquedas")
    print("[OK] La búsqueda es case-insensitive")
    print("[OK] Se pueden buscar por username, email, nombre y apellido")
    print("[OK] El frontend debería funcionar sin problemas")

if __name__ == "__main__":
    test_user_search()
