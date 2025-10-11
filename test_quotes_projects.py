#!/usr/bin/env python3
"""
Script para verificar el flujo cotizaciones → proyectos
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_quotes_projects():
    """Verificar cotizaciones y proyectos"""
    
    session = requests.Session()
    
    print("=== VERIFICACION COTIZACIONES A PROYECTOS ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener cotizaciones
    print("\n2. Verificando cotizaciones...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    print(f"   Status: {quotes_response.status_code}")
    
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        print(f"   [OK] Cotizaciones encontradas: {len(quotes)}")
        
        approved_quotes = [q for q in quotes if q['status'] == 'approved']
        print(f"   [OK] Cotizaciones aprobadas: {len(approved_quotes)}")
        
        for quote in quotes:
            print(f"      - ID: {quote['id']}, Título: {quote['title']}, Estado: {quote['status']}")
    else:
        print(f"   [ERROR] Error obteniendo cotizaciones: {quotes_response.text}")
        return
    
    # 3. Obtener proyectos
    print("\n3. Verificando proyectos...")
    projects_response = session.get(f"{BASE_URL}/branding/projects/")
    print(f"   Status: {projects_response.status_code}")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"   [OK] Proyectos encontrados: {len(projects)}")
        
        for project in projects:
            print(f"      - ID: {project['id']}, Título: {project['title']}, Estado: {project['status']}")
    else:
        print(f"   [ERROR] Error obteniendo proyectos: {projects_response.text}")
        return
    
    # 4. Analizar el problema
    print("\n4. Análisis del problema:")
    if len(approved_quotes) > 0 and len(projects) == 0:
        print("   [PROBLEMA] Hay cotizaciones aprobadas pero no hay proyectos")
        print("   [CAUSA] Las cotizaciones aprobadas no están creando proyectos automáticamente")
    elif len(approved_quotes) == len(projects):
        print("   [OK] Número de cotizaciones aprobadas coincide con proyectos")
    else:
        print("   [WARNING] Hay diferencia entre cotizaciones aprobadas y proyectos")
    
    # 5. Verificar si hay campo linked_project en cotizaciones
    print("\n5. Verificando campo linked_project en cotizaciones...")
    for quote in quotes:
        linked_project = quote.get('linked_project')
        print(f"      - Cotización ID {quote['id']}: linked_project = {linked_project}")
    
    print("\n=== CONCLUSIÓN ===")
    if len(approved_quotes) > 0 and len(projects) == 0:
        print("PROBLEMA: Las cotizaciones aprobadas no están creando proyectos.")
        print("SOLUCIÓN: Verificar el endpoint de aprobar cotizaciones.")
    else:
        print("El flujo cotizaciones → proyectos parece estar funcionando.")

if __name__ == "__main__":
    test_quotes_projects()
