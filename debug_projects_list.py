#!/usr/bin/env python3
"""
Script para debuggear el listado de proyectos
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def debug_projects_list():
    """Debuggear por qué el listado no muestra proyectos completados"""
    
    session = requests.Session()
    
    print("=== DEBUG LISTADO DE PROYECTOS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener todos los proyectos
    print("\n2. Obteniendo lista de proyectos...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    print(f"   Status: {projects_response.status_code}")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"   [OK] Total proyectos en lista: {len(projects)}")
        
        print("\n   --- PROYECTOS EN LA LISTA ---")
        for i, project in enumerate(projects):
            print(f"      {i+1}. ID: {project['id']}, Status: {project['status']}, Title: {project['title']}")
        
        # Verificar proyecto específico
        print(f"\n3. Verificando proyecto ID 1 individualmente...")
        project_1_response = session.get(f"{BASE_URL}/branding/projects/1/")
        print(f"   Status: {project_1_response.status_code}")
        
        if project_1_response.status_code == 200:
            project_1 = project_1_response.json()
            print(f"   [OK] Proyecto 1 individual: Status={project_1['status']}, Title={project_1['title']}")
            
            # Comparar
            if len(projects) > 0:
                project_in_list = next((p for p in projects if p['id'] == 1), None)
                if project_in_list:
                    print(f"   [INFO] Proyecto 1 en lista: Status={project_in_list['status']}")
                    if project_1['status'] != project_in_list['status']:
                        print(f"   [PROBLEMA] Estados diferentes: Individual={project_1['status']}, Lista={project_in_list['status']}")
                    else:
                        print(f"   [OK] Estados coinciden")
                else:
                    print(f"   [PROBLEMA] Proyecto ID 1 no está en la lista")
            else:
                print(f"   [PROBLEMA] La lista está vacía")
        else:
            print(f"   [ERROR] Error obteniendo proyecto individual: {project_1_response.text}")
    else:
        print(f"   [ERROR] Error obteniendo lista: {projects_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("Si el proyecto individual muestra 'completed' pero no aparece en la lista,")
    print("puede ser un problema de filtrado en el backend.")

if __name__ == "__main__":
    debug_projects_list()
