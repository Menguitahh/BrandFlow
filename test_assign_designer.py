#!/usr/bin/env python3
"""
Script para probar la asignación de diseñador
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_assign_designer():
    """Probar la asignación de diseñador"""
    
    session = requests.Session()
    
    print("=== PRUEBA DE ASIGNACIÓN DE DISEÑADOR ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener proyectos
    print("\n2. Obteniendo proyectos...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    print(f"   Status: {projects_response.status_code}")
    
    if projects_response.status_code != 200:
        print(f"   [ERROR] Error obteniendo proyectos: {projects_response.text}")
        return
    
    projects = projects_response.json()
    print(f"   [OK] Proyectos encontrados: {len(projects)}")
    
    if not projects:
        print("   [ERROR] No hay proyectos disponibles")
        return
    
    project = projects[0]
    print(f"   Proyecto seleccionado: ID {project['id']}, Título: {project['title']}")
    
    # 3. Obtener diseñadores
    print("\n3. Obteniendo diseñadores...")
    designers_response = session.get(f"{BASE_URL}/user/admin/designers/")
    print(f"   Status: {designers_response.status_code}")
    
    if designers_response.status_code != 200:
        print(f"   [ERROR] Error obteniendo diseñadores: {designers_response.text}")
        return
    
    designers_data = designers_response.json()
    designers = designers_data.get('designers', [])
    print(f"   [OK] Diseñadores encontrados: {len(designers)}")
    
    if not designers:
        print("   [ERROR] No hay diseñadores disponibles")
        return
    
    designer = designers[0]
    print(f"   Diseñador seleccionado: ID {designer['id']}, Nombre: {designer['username']}")
    
    # 4. Intentar asignar diseñador
    print(f"\n4. Asignando diseñador {designer['username']} al proyecto {project['title']}...")
    assign_data = {"designer_id": designer['id']}
    
    assign_response = session.post(
        f"{BASE_URL}/branding/projects/{project['id']}/assign_designer/", 
        json=assign_data
    )
    
    print(f"   Status: {assign_response.status_code}")
    print(f"   Response: {assign_response.text}")
    
    if assign_response.status_code == 200:
        print("   [OK] Diseñador asignado exitosamente")
    else:
        print("   [ERROR] Error asignando diseñador")
        print(f"   Error details: {assign_response.text}")
    
    print("\n=== CONCLUSIÓN ===")
    if assign_response.status_code == 500:
        print("Error 500 - Problema interno del servidor")
        print("Revisar logs del servidor Django")
    elif assign_response.status_code == 404:
        print("Error 404 - Endpoint no encontrado")
    elif assign_response.status_code == 403:
        print("Error 403 - Permisos insuficientes")
    elif assign_response.status_code == 400:
        print("Error 400 - Datos inválidos")

if __name__ == "__main__":
    test_assign_designer()
