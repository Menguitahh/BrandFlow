#!/usr/bin/env python3
"""
Script para simular exactamente lo que está enviando el frontend
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_frontend_data():
    """Simular los datos que está enviando el frontend"""
    
    session = requests.Session()
    
    print("=== SIMULANDO DATOS DEL FRONTEND ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener categorías disponibles
    print("\n2. Obteniendo categorías...")
    categories_response = session.get(f"{BASE_URL}/branding/service-categories/")
    
    if categories_response.status_code != 200:
        print(f"   [ERROR] No se pudieron obtener categorías: {categories_response.status_code}")
        return
    
    categories = categories_response.json()
    if not categories:
        print("   [ERROR] No hay categorías disponibles")
        return
    
    category_id = categories[0]['id']
    print(f"   [OK] Usando categoría: {categories[0]['name']} (ID: {category_id})")
    
    # 3. Probar con el formato INCORRECTO (lo que está enviando el frontend)
    print("\n3. Probando con formato INCORRECTO (category)...")
    service_data_wrong = {
        "name": "Servicio Frontend Test",
        "description": "Descripción de prueba",
        "service_type": "test",
        "base_price": 100,
        "features": ["Feature 1", "Feature 2"],
        "delivery_time": "2-3 días",
        "category": category_id  # INCORRECTO - debería ser category_id
    }
    
    response_wrong = session.post(f"{BASE_URL}/branding/services/", json=service_data_wrong)
    print(f"   Status: {response_wrong.status_code}")
    print(f"   Response: {response_wrong.text}")
    
    # 4. Probar con el formato CORRECTO
    print("\n4. Probando con formato CORRECTO (category_id)...")
    service_data_correct = {
        "name": "Servicio Frontend Test Correcto",
        "description": "Descripción de prueba",
        "service_type": "test",
        "base_price": 100,
        "features": ["Feature 1", "Feature 2"],
        "delivery_time": "2-3 días",
        "category_id": category_id  # CORRECTO
    }
    
    response_correct = session.post(f"{BASE_URL}/branding/services/", json=service_data_correct)
    print(f"   Status: {response_correct.status_code}")
    print(f"   Response: {response_correct.text}")
    
    if response_correct.status_code == 201:
        service = response_correct.json()
        print(f"   [OK] Servicio creado: ID {service['id']}, Nombre: {service['name']}")
    
    print("\n=== CONCLUSIÓN ===")
    print("El frontend debe cambiar 'category' por 'category_id' en el JSON que envía")

if __name__ == "__main__":
    test_frontend_data()

