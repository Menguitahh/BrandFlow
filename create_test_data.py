#!/usr/bin/env python3
"""
Script para crear datos de prueba para el admin
"""
import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrandFlow.settings')
django.setup()

from user_control.models import Users
from brand_control.models import Service, ServiceCategory, QuoteRequest, Project

def create_test_data():
    """Crear datos de prueba para testing"""
    
    print("Creando datos de prueba...")
    
    # 1. Crear algunos diseñadores
    print("1. Creando diseñadores...")
    designers_data = [
        {
            'username': 'juan_designer',
            'email': 'juan@designer.com',
            'password': 'Designer123!',
            'first_name': 'Juan',
            'last_name': 'Diseñador',
            'roles': 'diseñador'
        },
        {
            'username': 'maria_creative',
            'email': 'maria@creative.com', 
            'password': 'Creative123!',
            'first_name': 'María',
            'last_name': 'Creativa',
            'roles': 'diseñador'
        },
        {
            'username': 'carlos_art',
            'email': 'carlos@art.com',
            'password': 'Art123!',
            'first_name': 'Carlos',
            'last_name': 'Artista',
            'roles': 'diseñador'
        }
    ]
    
    for designer_data in designers_data:
        designer, created = Users.objects.get_or_create(
            username=designer_data['username'],
            defaults=designer_data
        )
        if created:
            designer.set_password(designer_data['password'])
            designer.save()
            print(f"   Creado: {designer.username} ({designer.roles})")
        else:
            print(f"   Ya existe: {designer.username}")
    
    # 2. Crear algunos clientes adicionales
    print("\n2. Creando clientes adicionales...")
    clients_data = [
        {
            'username': 'empresa_abc',
            'email': 'contacto@empresaabc.com',
            'password': 'Client123!',
            'first_name': 'Empresa',
            'last_name': 'ABC',
            'roles': 'cliente'
        },
        {
            'username': 'startup_xyz',
            'email': 'info@startupxyz.com',
            'password': 'Startup123!',
            'first_name': 'Startup',
            'last_name': 'XYZ',
            'roles': 'cliente'
        }
    ]
    
    for client_data in clients_data:
        client, created = Users.objects.get_or_create(
            username=client_data['username'],
            defaults=client_data
        )
        if created:
            client.set_password(client_data['password'])
            client.save()
            print(f"   Creado: {client.username} ({client.roles})")
        else:
            print(f"   Ya existe: {client.username}")
    
    # 3. Crear algunas cotizaciones
    print("\n3. Creando cotizaciones...")
    
    # Obtener servicios y clientes
    logo_service = Service.objects.filter(name__icontains='Logo Básico').first()
    web_service = Service.objects.filter(name__icontains='Landing Page').first()
    client1 = Users.objects.filter(username='empresa_abc').first()
    client2 = Users.objects.filter(username='startup_xyz').first()
    
    if logo_service and client1:
        quote1, created = QuoteRequest.objects.get_or_create(
            title="Logo para Empresa ABC",
            defaults={
                'client': client1,
                'service': logo_service,
                'description': 'Necesitamos un logo moderno para nuestra empresa de tecnología',
                'budget': 200,
                'status': 'pending'
            }
        )
        if created:
            print(f"   Cotización creada: {quote1.title}")
    
    if web_service and client2:
        quote2, created = QuoteRequest.objects.get_or_create(
            title="Landing Page para Startup",
            defaults={
                'client': client2,
                'service': web_service,
                'description': 'Landing page para lanzamiento de producto',
                'budget': 500,
                'status': 'pending'
            }
        )
        if created:
            print(f"   Cotización creada: {quote2.title}")
    
    # 4. Crear algunos proyectos (después de aprobar cotizaciones)
    print("\n4. Creando proyectos...")
    
    # Aprobar cotizaciones y crear proyectos
    if 'quote1' in locals() and quote1:
        quote1.status = 'approved'
        quote1.save()
        
        project1, created = Project.objects.get_or_create(
            title=quote1.title,
            defaults={
                'client': quote1.client,
                'service': quote1.service,
                'brief': quote1.description,
                'status': 'quote',
                'total_price': quote1.budget
            }
        )
        if created:
            print(f"   Proyecto creado: {project1.title}")
    
    if 'quote2' in locals() and quote2:
        quote2.status = 'approved'
        quote2.save()
        
        project2, created = Project.objects.get_or_create(
            title=quote2.title,
            defaults={
                'client': quote2.client,
                'service': quote2.service,
                'brief': quote2.description,
                'status': 'quote',
                'total_price': quote2.budget
            }
        )
        if created:
            print(f"   Proyecto creado: {project2.title}")
    
    print("\nDatos de prueba creados exitosamente!")
    print("\nCredenciales de prueba:")
    print("Diseñadores:")
    print("  - juan_designer / Designer123!")
    print("  - maria_creative / Creative123!")
    print("  - carlos_art / Art123!")
    print("\nClientes:")
    print("  - empresa_abc / Client123!")
    print("  - startup_xyz / Startup123!")

if __name__ == "__main__":
    create_test_data()

