#!/usr/bin/env python3
"""
Script para crear una cotización pendiente para pruebas
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def create_pending_quote():
    """Crear una cotización pendiente para pruebas"""
    
    session = requests.Session()
    
    print("=== CREANDO COTIZACION PENDIENTE PARA PRUEBAS ===")
    
    # 1. Login como cliente
    print("\n1. Login como cliente...")
    login_data = {"identifier": "test_client", "password": "test123"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        print("   Intentando con otro usuario...")
        
        # Intentar con admin
        login_data = {"identifier": "admin", "password": "Admin123!"}
        login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
        
        if login_response.status_code != 200:
            print(f"   [ERROR] Login admin también falló: {login_response.status_code}")
            return
    
    print("   [OK] Login exitoso")
    
    # 2. Crear cotización pendiente
    print("\n2. Creando cotización pendiente...")
    quote_data = {
        "title": "Logo para Restaurante Nuevo",
        "description": "Necesitamos un logo moderno y elegante para nuestro nuevo restaurante italiano. Debe incluir elementos relacionados con la comida italiana y transmitir calidez y calidad.",
        "budget": 350.00,
        "service": 1  # Servicio de logo
    }
    
    quote_response = session.post(f"{BASE_URL}/branding/quotes/", json=quote_data)
    print(f"   Status: {quote_response.status_code}")
    
    if quote_response.status_code == 201:
        quote = quote_response.json()
        print(f"   [OK] Cotización creada exitosamente")
        print(f"   ID: {quote['id']}")
        print(f"   Título: {quote['title']}")
        print(f"   Estado: {quote['status']}")
        print(f"   Presupuesto: €{quote['budget']}")
    else:
        print(f"   [ERROR] Error creando cotización: {quote_response.text}")
        return
    
    # 3. Verificar que se creó correctamente
    print("\n3. Verificando cotización creada...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        pending_quotes = [q for q in quotes if q['status'] == 'pending']
        print(f"   [OK] Total cotizaciones: {len(quotes)}")
        print(f"   [OK] Cotizaciones pendientes: {len(pending_quotes)}")
        
        for quote in pending_quotes:
            print(f"      - ID: {quote['id']}, Título: {quote['title']}, Estado: {quote['status']}")
    else:
        print(f"   [ERROR] Error verificando cotizaciones: {quotes_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("Ahora deberías tener una cotización pendiente en el frontend.")
    print("Ve a 'Revisión de Cotizaciones' para verla y probar las funcionalidades.")

if __name__ == "__main__":
    create_pending_quote()
