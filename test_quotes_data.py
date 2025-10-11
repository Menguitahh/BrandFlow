#!/usr/bin/env python3
"""
Script para verificar la estructura de datos de cotizaciones
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_quotes_data():
    """Verificar estructura de datos de cotizaciones"""
    
    session = requests.Session()
    
    print("=== VERIFICACION ESTRUCTURA DE COTIZACIONES ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener cotizaciones con detalles
    print("\n2. Verificando estructura de datos de cotizaciones...")
    quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
    print(f"   Status: {quotes_response.status_code}")
    
    if quotes_response.status_code == 200:
        quotes = quotes_response.json()
        print(f"   [OK] Cotizaciones encontradas: {len(quotes)}")
        
        for i, quote in enumerate(quotes):
            print(f"\n   --- COTIZACION {i+1} ---")
            print(f"   ID: {quote.get('id')}")
            print(f"   Título: {quote.get('title')}")
            print(f"   Descripción: {quote.get('description')}")
            print(f"   Estado: {quote.get('status')}")
            print(f"   Presupuesto: {quote.get('budget')}")
            print(f"   Cliente: {quote.get('client')} (tipo: {type(quote.get('client'))})")
            print(f"   Servicio: {quote.get('service')} (tipo: {type(quote.get('service'))})")
            print(f"   Fecha: {quote.get('created_at')}")
            print(f"   Campos disponibles: {list(quote.keys())}")
            
            # Verificar si cliente y servicio son objetos o IDs
            client = quote.get('client')
            service = quote.get('service')
            
            if isinstance(client, dict):
                print(f"   Cliente (objeto): {client}")
            else:
                print(f"   Cliente (ID): {client}")
                
            if isinstance(service, dict):
                print(f"   Servicio (objeto): {service}")
            else:
                print(f"   Servicio (ID): {service}")
    else:
        print(f"   [ERROR] Error obteniendo cotizaciones: {quotes_response.text}")
        return
    
    print("\n=== CONCLUSION ===")
    print("El frontend espera objetos completos pero el backend devuelve solo IDs.")
    print("Necesitamos ajustar el frontend o el backend para que coincidan.")

if __name__ == "__main__":
    test_quotes_data()
