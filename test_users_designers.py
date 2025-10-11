#!/usr/bin/env python3
"""
Script para verificar usuarios y diseñadores
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_users_designers():
    """Verificar usuarios y diseñadores disponibles"""
    
    session = requests.Session()
    
    print("=== VERIFICACION DE USUARIOS Y DISEÑADORES ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener usuarios
    print("\n2. Obteniendo usuarios...")
    users_response = session.get(f"{BASE_URL}/user/admin/users/")
    print(f"   Status: {users_response.status_code}")
    
    if users_response.status_code == 200:
        users_data = users_response.json()
        users_list = users_data.get('users', users_data) if isinstance(users_data, dict) else users_data
        
        print(f"   [OK] Total usuarios: {len(users_list)}")
        
        # Mostrar todos los usuarios
        print("\n   --- TODOS LOS USUARIOS ---")
        for user in users_list:
            print(f"      - ID: {user['id']}, Username: {user['username']}, Role: {user.get('role', 'N/A')}")
        
        # Filtrar diseñadores
        designers = [u for u in users_list if u.get('role') == 'diseñador']
        print(f"\n   [OK] Diseñadores encontrados: {len(designers)}")
        
        if designers:
            print("\n   --- DISEÑADORES ---")
            for designer in designers:
                print(f"      - ID: {designer['id']}, Username: {designer['username']}, Role: {designer['role']}")
        else:
            print("   [INFO] No hay usuarios con rol 'diseñador'")
            print("   [SUGERENCIA] Crear usuarios con rol diseñador para probar la funcionalidad")
    else:
        print(f"   [ERROR] Error obteniendo usuarios: {users_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("El frontend ahora filtrará automáticamente los usuarios con rol 'diseñador'.")

if __name__ == "__main__":
    test_users_designers()
