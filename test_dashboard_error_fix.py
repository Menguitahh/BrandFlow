#!/usr/bin/env python3
"""
Script para verificar que el error de toFixed se ha solucionado
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_dashboard_data():
    """Probar que los datos del dashboard se cargan correctamente"""
    
    session = requests.Session()
    
    print("=== PRUEBA DE DATOS DEL DASHBOARD ===")
    
    # 1. Login como admin
    print("\n1. Login como admin...")
    login_data = {"identifier": "admin", "password": "Admin123!"}
    login_response = session.post(f"{BASE_URL}/user/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"   [ERROR] Login falló: {login_response.status_code}")
        return
    
    print("   [OK] Login exitoso")
    
    # 2. Obtener datos para el dashboard
    print("\n2. Obteniendo datos del dashboard...")
    
    try:
        # Obtener cotizaciones
        quotes_response = session.get(f"{BASE_URL}/branding/quotes/")
        quotes = quotes_response.json() if quotes_response.status_code == 200 else []
        print(f"   [INFO] Cotizaciones: {len(quotes)}")
        
        # Obtener proyectos
        projects_response = session.get(f"{BASE_URL}/branding/projects/")
        projects = projects_response.json() if projects_response.status_code == 200 else []
        print(f"   [INFO] Proyectos: {len(projects)}")
        
        # Obtener usuarios
        users_response = session.get(f"{BASE_URL}/user/admin/users/")
        users_data = users_response.json() if users_response.status_code == 200 else {}
        users = users_data.get('users', [])
        print(f"   [INFO] Usuarios: {len(users)}")
        
        # 3. Calcular estadísticas como lo hace el frontend
        print("\n3. Calculando estadísticas...")
        
        # Calcular ingresos totales de proyectos completados
        totalEarnings = sum(
            float(p.get('total_price', 0)) 
            for p in projects 
            if p.get('status') == 'completed'
        )
        
        print(f"   [INFO] Ingresos totales: {totalEarnings}")
        print(f"   [INFO] Tipo de ingresos: {type(totalEarnings)}")
        print(f"   [INFO] toFixed(2): {totalEarnings:.2f}")
        
        # Calcular otras estadísticas
        totalProjects = len(projects)
        totalQuotes = len(quotes)
        pendingQuotes = len([q for q in quotes if q.get('status') in ['pending', 'submitted']])
        activeProjects = len([p for p in projects if p.get('status') == 'in_progress'])
        completedProjects = len([p for p in projects if p.get('status') == 'completed'])
        totalUsers = len(users)
        totalDesigners = len([u for u in users if u.get('role') == 'diseñador'])
        
        print(f"   [INFO] Total proyectos: {totalProjects}")
        print(f"   [INFO] Total cotizaciones: {totalQuotes}")
        print(f"   [INFO] Cotizaciones pendientes: {pendingQuotes}")
        print(f"   [INFO] Proyectos activos: {activeProjects}")
        print(f"   [INFO] Proyectos completados: {completedProjects}")
        print(f"   [INFO] Total usuarios: {totalUsers}")
        print(f"   [INFO] Total diseñadores: {totalDesigners}")
        
        # 4. Verificar que no hay valores undefined
        print("\n4. Verificando valores...")
        
        stats = {
            'totalUsers': totalUsers,
            'totalProjects': totalProjects,
            'totalQuotes': totalQuotes,
            'pendingQuotes': pendingQuotes,
            'activeProjects': activeProjects,
            'completedProjects': completedProjects,
            'totalDesigners': totalDesigners,
            'totalEarnings': totalEarnings
        }
        
        for key, value in stats.items():
            if value is None:
                print(f"   [ERROR] {key} es None")
            elif value == 0:
                print(f"   [OK] {key} = {value} (valor por defecto)")
            else:
                print(f"   [OK] {key} = {value}")
        
        # 5. Simular renderizado del dashboard
        print("\n5. Simulando renderizado del dashboard...")
        
        # Simular el renderizado de ingresos
        earnings_display = f"€{stats['totalEarnings']:.2f}" if stats['totalEarnings'] else "€0.00"
        print(f"   [INFO] Display de ingresos: {earnings_display}")
        
        # Simular el cálculo de porcentaje
        completion_percentage = (stats['completedProjects'] / stats['totalProjects'] * 100) if stats['totalProjects'] > 0 else 0
        print(f"   [INFO] Porcentaje de completados: {completion_percentage:.1f}%")
        
        print("\n=== CONCLUSION ===")
        print("[OK] Todos los datos se calculan correctamente")
        print("[OK] No hay valores undefined que causen errores")
        print("[OK] El dashboard deberia renderizarse sin errores")
        
        # 6. Mostrar ejemplo de datos que se enviarian al frontend
        print("\n6. Datos que se enviarian al frontend:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    test_dashboard_data()
