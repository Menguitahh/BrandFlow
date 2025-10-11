#!/usr/bin/env python3
"""
Script para probar la persistencia de proyectos completados
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_project_persistence():
    """Probar si los proyectos completados se guardan correctamente"""
    
    session = requests.Session()
    
    print("=== PRUEBA DE PERSISTENCIA DE PROYECTOS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Verificar estado actual del proyecto 1
    print("\n2. Verificando estado actual del proyecto 1...")
    project_response = session.get(f"{BASE_URL}/branding/projects/1/")
    print(f"   Status: {project_response.status_code}")
    
    if project_response.status_code == 200:
        project = project_response.json()
        print(f"   [INFO] Estado actual: {project['status']}")
        print(f"   [INFO] Actualizado en: {project['updated_at']}")
        
        # 3. Intentar completar el proyecto
        print(f"\n3. Completando proyecto...")
        complete_data = {
            'title': project['title'],
            'brief': project.get('brief', ''),
            'status': 'completed',
            'total_price': float(project.get('total_price', 0)),
            'service': project['service'],
            'delivery_date': project.get('delivery_date')
        }
        
        print(f"   [INFO] Datos enviados: {complete_data}")
        complete_response = session.put(f"{BASE_URL}/branding/projects/1/", json=complete_data)
        print(f"   [INFO] Respuesta status: {complete_response.status_code}")
        
        if complete_response.status_code == 200:
            result = complete_response.json()
            print(f"   [OK] Estado después de completar: {result['status']}")
            print(f"   [OK] Actualizado en: {result['updated_at']}")
            
            # 4. Verificar inmediatamente después
            print(f"\n4. Verificando inmediatamente después...")
            verify_response = session.get(f"{BASE_URL}/branding/projects/1/")
            
            if verify_response.status_code == 200:
                verify_project = verify_response.json()
                print(f"   [INFO] Estado verificado: {verify_project['status']}")
                print(f"   [INFO] Actualizado en: {verify_project['updated_at']}")
                
                if verify_project['status'] == 'completed':
                    print(f"   [OK] Proyecto se mantiene como completado")
                else:
                    print(f"   [PROBLEMA] Proyecto volvió a estado: {verify_project['status']}")
            else:
                print(f"   [ERROR] Error verificando: {verify_response.text}")
        else:
            print(f"   [ERROR] Error completando: {complete_response.text}")
    else:
        print(f"   [ERROR] Error obteniendo proyecto: {project_response.text}")
    
    # 5. Verificar lista de proyectos
    print(f"\n5. Verificando lista de proyectos...")
    list_response = session.get(f"{BASE_URL}/branding/projects/")
    
    if list_response.status_code == 200:
        projects = list_response.json()
        print(f"   [INFO] Total proyectos en lista: {len(projects)}")
        
        for project in projects:
            if project['id'] == 1:
                print(f"   [INFO] Proyecto 1 en lista: Status={project['status']}")
                break
    else:
        print(f"   [ERROR] Error obteniendo lista: {list_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("Si el proyecto se completa pero vuelve a su estado anterior,")
    print("puede ser un problema de:")
    print("1. Transacciones de base de datos")
    print("2. Serializer que no guarda el estado")
    print("3. Caché o middleware que revierte cambios")

if __name__ == "__main__":
    test_project_persistence()
