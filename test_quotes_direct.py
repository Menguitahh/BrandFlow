#!/usr/bin/env python3
"""
Script para verificar cotizaciones directamente
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_quotes_direct():
    """Verificar cotizaciones directamente"""
    
    session = requests.Session()
    
    print("=== VERIFICACION DIRECTA DE COTIZACIONES ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener cotizaciones directamente
    print("\n2. Obteniendo cotizaciones...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    print(f"   Status: {quotes_response.status_code}")
    
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        print(f"   [OK] Total cotizaciones: {len(quotes)}")
        
        for quote in quotes:
            print(f"      - ID: {quote['id']}, Título: {quote['title']}, Estado: {quote['status']}")
            
            # Verificar si es la nueva cotización
            if quote['title'] == 'Logo para Restaurante Nuevo':
                print(f"         [ENCONTRADA] Nueva cotización creada")
                print(f"         Cliente: {quote['client']}")
                print(f"         Servicio: {quote['service']}")
                print(f"         Presupuesto: {quote['budget']}")
    else:
        print(f"   [ERROR] Error obteniendo cotizaciones: {quotes_response.text}")
    
    print("\n=== CONCLUSION ===")
    print("Si la nueva cotización no aparece, puede ser un problema de filtrado en el backend.")

if __name__ == "__main__":
    test_quotes_direct()
