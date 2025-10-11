#!/usr/bin/env python3
"""
Script para completar un proyecto manualmente y verificar el dashboard
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def complete_project_manually():
    """Completar un proyecto manualmente para probar el dashboard"""
    
    session = requests.Session()
    
    print("=== COMPLETANDO PROYECTO MANUALMENTE ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener proyectos actuales
    print("\n2. Obteniendo proyectos actuales...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"   [OK] Total proyectos: {len(projects)}")
        
        # Buscar un proyecto en progreso para completar
        in_progress_projects = [p for p in projects if p.get('status') == 'in_progress']
        
        if in_progress_projects:
            project = in_progress_projects[0]
            print(f"   [OK] Proyecto encontrado para completar: {project['title']}")
            
            # 3. Completar el proyecto
            print(f"\n3. Completando proyecto ID {project['id']}...")
            complete_data = {
                'title': project['title'],
                'brief': project.get('brief', ''),
                'status': 'completed',
                'total_price': float(project.get('total_price', 0)),
                'service': project['service'],
                'delivery_date': project.get('delivery_date')
            }
            
            complete_response = session.put(f"{BASE_URL}/branding/projects/{project['id']}/", json=complete_data)
            print(f"   Status: {complete_response.status_code}")
            
            if complete_response.status_code == 200:
                print("   [OK] Proyecto completado exitosamente")
                
                # 4. Verificar que se completó
                print(f"\n4. Verificando proyecto completado...")
                verify_response = session.get(f"{BASE_URL}/branding/projects/")
                
                if verify_response.status_code == 200:
                    updated_projects = verify_response.json()
                    completed_projects = [p for p in updated_projects if p.get('status') == 'completed']
                    
                    print(f"   [OK] Proyectos completados: {len(completed_projects)}")
                    
                    total_earnings = sum(float(p.get('total_price', 0)) for p in completed_projects)
                    print(f"   [OK] Ingresos totales: €{total_earnings:.2f}")
                    
                    print("\n   --- PROYECTOS COMPLETADOS ---")
                    for p in completed_projects:
                        print(f"      - ID: {p['id']}, Título: {p['title']}, Precio: €{p['total_price']}")
                else:
                    print(f"   [ERROR] Error verificando: {verify_response.text}")
            else:
                print(f"   [ERROR] Error completando proyecto: {complete_response.text}")
        else:
            print("   [INFO] No hay proyectos en progreso para completar")
            print("   [SUGERENCIA] Primero asigna un diseñador a un proyecto")
    else:
        print(f"   [ERROR] Error obteniendo proyectos: {projects_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("Si el proyecto se completó exitosamente, el dashboard debería mostrar:")
    print("- Ingresos totales actualizados")
    print("- Progreso de completados actualizado")
    print("- Estadísticas precisas")

if __name__ == "__main__":
    complete_project_manually()
