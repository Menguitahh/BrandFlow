#!/usr/bin/env python3
"""
Script para verificar el estado de los proyectos
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_project_status():
    """Verificar el estado actual de los proyectos"""
    
    session = requests.Session()
    
    print("=== VERIFICACION ESTADO DE PROYECTOS ===")
    
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
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"   [OK] Total proyectos: {len(projects)}")
        
        # Analizar proyectos por estado
        completed_projects = [p for p in projects if p.get('status') == 'completed']
        in_progress_projects = [p for p in projects if p.get('status') == 'in_progress']
        quote_projects = [p for p in projects if p.get('status') == 'quote']
        
        print(f"   [OK] Proyectos completados: {len(completed_projects)}")
        print(f"   [OK] Proyectos en progreso: {len(in_progress_projects)}")
        print(f"   [OK] Proyectos en cotización: {len(quote_projects)}")
        
        # Calcular ingresos totales
        total_earnings = sum(float(p.get('total_price', 0)) for p in completed_projects)
        print(f"   [OK] Ingresos totales: €{total_earnings:.2f}")
        
        print("\n   --- DETALLES DE PROYECTOS ---")
        for project in projects:
            print(f"      - ID: {project['id']}, Título: {project['title']}, Estado: {project['status']}, Precio: €{project['total_price']}")
    else:
        print(f"   [ERROR] Error obteniendo proyectos: {projects_response.text}")
    
    print("\n=== CONCLUSION ===")
    if projects_response.status_code == 200:
        projects = projects_response.json()
        completed_count = len([p for p in projects if p.get('status') == 'completed'])
        if completed_count > 0:
            print("✅ Hay proyectos completados en el backend")
            print("El problema puede ser que el dashboard no se está refrescando")
        else:
            print("❌ No hay proyectos completados en el backend")
            print("El proyecto no se completó correctamente")

if __name__ == "__main__":
    test_project_status()
