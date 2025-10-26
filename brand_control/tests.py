from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import json

from .models import ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage


class BrandingTestCase(APITestCase):
    """Pruebas para las funcionalidades de branding"""
    
    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        # Crear usuario admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            roles='admin'
        )
        
        # Crear usuario cliente
        self.client_user = User.objects.create_user(
            username='cliente',
            email='cliente@test.com',
            password='cliente123',
            roles='cliente'
        )
        
        # Crear usuario diseñador
        self.designer_user = User.objects.create_user(
            username='diseñador',
            email='diseñador@test.com',
            password='diseñador123',
            roles='diseñador'
        )
        
        # Crear categoría de servicio
        self.service_category = ServiceCategory.objects.create(
            name='Diseño Gráfico',
            description='Servicios de diseño gráfico'
        )
        
        # Crear servicio
        self.service = Service.objects.create(
            category=self.service_category,
            name='Diseño de Logo',
            description='Diseño profesional de logotipos',
            base_price=Decimal('150.00'),
            delivery_time='5-7 días'
        )
        
        # Configurar cliente API
        self.client = APIClient()
    
    def test_1_service_creation(self):
        """Prueba 1: Creación de servicios"""
        print("\n=== PRUEBA 1: CREACIÓN DE SERVICIOS ===")
        
        # Login como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Crear nuevo servicio
        service_data = {
            'category_id': self.service_category.id,
            'name': 'Identidad Corporativa',
            'description': 'Diseño completo de identidad corporativa',
            'base_price': '400.00',
            'delivery_time': '10-14 días'
        }
        
        url = reverse('services-list')
        response = self.client.post(url, service_data, format='json')
        
        print(f"Respuesta de creación de servicio: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que se creó exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el servicio existe en la base de datos
        self.assertTrue(Service.objects.filter(name='Identidad Corporativa').exists())
        
        print("Creación de servicio exitosa")
    
    def test_2_quote_request_creation(self):
        """Prueba 2: Creación de solicitud de cotización"""
        print("\n=== PRUEBA 2: CREACIÓN DE SOLICITUD DE COTIZACIÓN ===")
        
        # Login como cliente
        self.client.force_authenticate(user=self.client_user)
        
        # Crear solicitud de cotización
        quote_data = {
            'service': self.service.id,
            'title': 'Logo para mi empresa',
            'description': 'Necesito un logo moderno para mi startup tecnológica',
            'budget': '200.00'
        }
        
        url = reverse('quotes-list')
        response = self.client.post(url, quote_data, format='json')
        
        print(f"Respuesta de creación de cotización: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que se creó exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que la cotización existe en la base de datos
        self.assertTrue(QuoteRequest.objects.filter(title='Logo para mi empresa').exists())
        
        print("Creación de cotización exitosa")
    
    def test_3_quote_approval_and_project_creation(self):
        """Prueba 3: Aprobación de cotización y creación de proyecto"""
        print("\n=== PRUEBA 3: APROBACIÓN DE COTIZACIÓN ===")
        
        # Crear cotización
        quote = QuoteRequest.objects.create(
            client=self.client_user,
            service=self.service,
            title='Logo para mi empresa',
            description='Necesito un logo moderno',
            budget=Decimal('200.00')
        )
        
        # Login como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Aprobar cotización
        url = reverse('quotes-approve', kwargs={'pk': quote.id})
        response = self.client.post(url, format='json')
        
        print(f"Respuesta de aprobación: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que se aprobó exitosamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se creó el proyecto
        quote.refresh_from_db()
        self.assertIsNotNone(quote.linked_project)
        self.assertEqual(quote.status, 'approved')
        
        print("Aprobación de cotización y creación de proyecto exitosa")
    
    def test_4_project_assignment(self):
        """Prueba 4: Asignación de diseñador a proyecto"""
        print("\n=== PRUEBA 4: ASIGNACIÓN DE DISEÑADOR ===")
        
        # Crear proyecto
        project = Project.objects.create(
            title='Logo para mi empresa',
            brief='Diseño de logo moderno',
            client=self.client_user,
            service=self.service,
            status='approved',
            total_price=Decimal('200.00')
        )
        
        # Login como admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Asignar diseñador
        url = reverse('projects-assign-designer', kwargs={'pk': project.id})
        response = self.client.post(url, {'designer_id': self.designer_user.id}, format='json')
        
        print(f"Respuesta de asignación: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que se asignó exitosamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el proyecto tiene diseñador asignado
        project.refresh_from_db()
        self.assertEqual(project.assigned_to, self.designer_user)
        self.assertEqual(project.status, 'in_progress')
        
        print("Asignación de diseñador exitosa")
    
    def test_5_simulated_payment(self):
        """Prueba 5: Pago simulado"""
        print("\n=== PRUEBA 5: PAGO SIMULADO ===")
        
        # Crear proyecto
        project = Project.objects.create(
            title='Logo para mi empresa',
            brief='Diseño de logo moderno',
            client=self.client_user,
            service=self.service,
            status='approved',
            total_price=Decimal('200.00')
        )
        
        # Login como cliente
        self.client.force_authenticate(user=self.client_user)
        
        # Realizar pago simulado
        url = reverse('payments-simulate')
        payment_data = {
            'project_id': project.id,
            'amount': '200.00',
            'cardholder_name': 'Juan Pérez',
            'card_last4': '1234'
        }
        response = self.client.post(url, payment_data, format='json')
        
        print(f"Respuesta de pago: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el pago se procesó exitosamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el proyecto se actualizó
        project.refresh_from_db()
        self.assertEqual(project.paid_amount, Decimal('200.00'))
        self.assertEqual(project.status, 'in_progress')
        
        # Verificar que se creó el pago
        self.assertTrue(Payment.objects.filter(project=project).exists())
        
        print("Pago simulado exitoso")
    
    def test_6_project_messages(self):
        """Prueba 6: Envío de mensajes en el proyecto"""
        print("\n=== PRUEBA 6: MENSAJES DEL PROYECTO ===")
        
        # Crear proyecto con diseñador asignado
        project = Project.objects.create(
            title='Logo para mi empresa',
            brief='Diseño de logo moderno',
            client=self.client_user,
            assigned_to=self.designer_user,
            service=self.service,
            status='in_progress',
            total_price=Decimal('200.00'),
            paid_amount=Decimal('200.00')
        )
        
        # Login como diseñador
        self.client.force_authenticate(user=self.designer_user)
        
        # Enviar mensaje
        url = reverse('project-messages-list', kwargs={'project_pk': project.id})
        message_data = {
            'message': 'Hola, he comenzado a trabajar en tu logo. ¿Te parece bien esta dirección?'
        }
        response = self.client.post(url, message_data, format='json')
        
        print(f"Respuesta de mensaje: {response.status_code}")
        print(f"Contenido de la respuesta: {response.data}")
        
        # Verificar que el mensaje se envió exitosamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el mensaje existe en la base de datos
        self.assertTrue(ProjectMessage.objects.filter(project=project).exists())
        
        print("Envío de mensaje exitoso")
    
    def test_7_project_completion_flow(self):
        """Prueba 7: Flujo completo de finalización de proyecto"""
        print("\n=== PRUEBA 7: FINALIZACIÓN DE PROYECTO ===")
        
        # Crear proyecto con diseñador asignado
        project = Project.objects.create(
            title='Logo para mi empresa',
            brief='Diseño de logo moderno',
            client=self.client_user,
            assigned_to=self.designer_user,
            service=self.service,
            status='in_progress',
            total_price=Decimal('200.00'),
            paid_amount=Decimal('200.00')
        )
        
        # Paso 1: Diseñador marca como completado
        self.client.force_authenticate(user=self.designer_user)
        url = reverse('projects-mark-completed-by-designer', kwargs={'pk': project.id})
        response = self.client.post(url, format='json')
        
        print(f"Respuesta de marcado como completado: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        project.refresh_from_db()
        self.assertEqual(project.status, 'pending_completion_confirmation')
        
        # Paso 2: Admin confirma finalización
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('projects-confirm-completion', kwargs={'pk': project.id})
        response = self.client.post(url, format='json')
        
        print(f"Respuesta de confirmación: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        project.refresh_from_db()
        self.assertEqual(project.status, 'completed')
        
        print("Flujo de finalización de proyecto exitoso")
    
    def test_8_complete_branding_workflow(self):
        """Prueba 8: Flujo completo de branding"""
        print("\n=== PRUEBA 8: FLUJO COMPLETO DE BRANDING ===")
        
        # 1. Cliente crea cotización
        self.client.force_authenticate(user=self.client_user)
        quote_data = {
            'service': self.service.id,
            'title': 'Logo completo',
            'description': 'Necesito logo y tarjetas de presentación',
            'budget': '300.00'
        }
        url = reverse('quotes-list')
        response = self.client.post(url, quote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote_id = response.data['id']
        
        # 2. Admin aprueba cotización
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('quotes-approve', kwargs={'pk': quote_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_id = response.data['project_id']
        
        # 3. Admin asigna diseñador
        url = reverse('projects-assign-designer', kwargs={'pk': project_id})
        response = self.client.post(url, {'designer_id': self.designer_user.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Cliente paga
        self.client.force_authenticate(user=self.client_user)
        url = reverse('payments-simulate')
        payment_data = {
            'project_id': project_id,
            'amount': '300.00',
            'cardholder_name': 'Juan Pérez',
            'card_last4': '1234'
        }
        response = self.client.post(url, payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Diseñador envía mensaje
        self.client.force_authenticate(user=self.designer_user)
        url = reverse('project-messages-list', kwargs={'project_pk': project_id})
        message_data = {'message': '¡Hola! He comenzado a trabajar en tu proyecto.'}
        response = self.client.post(url, message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 6. Diseñador marca como completado
        url = reverse('projects-mark-completed-by-designer', kwargs={'pk': project_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 7. Admin confirma finalización
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('projects-confirm-completion', kwargs={'pk': project_id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print("Flujo completo de branding exitoso")