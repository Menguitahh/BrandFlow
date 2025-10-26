from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializer import (
    ServiceCategorySerializer, ServiceSerializer, ProjectSerializer, QuoteRequestSerializer,
    PaymentSerializer, ProjectMessageSerializer
)
from .models import (
    ServiceCategory, Service, Project, QuoteRequest, Payment, ProjectMessage
)
from django.contrib.auth import get_user_model
from user_control.permissions import IsAdminUserCustom, IsAdmin, IsDesigner, IsProjectParticipant

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]


@method_decorator(csrf_exempt, name='dispatch')
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]


@method_decorator(csrf_exempt, name='dispatch')
class QuoteRequestViewSet(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            # Admin puede ver todas las cotizaciones
            return QuoteRequest.objects.all().order_by('-created_at')
        else:
            # Cliente solo ve las suyas
            return QuoteRequest.objects.filter(client=user).order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Aprobar cotización y crear proyecto"""
        quote = self.get_object()
        
        if quote.status != 'submitted':
            return Response({'detail': 'Solo se pueden aprobar cotizaciones en estado submitted'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Crear proyecto
        project_data = {
            'title': quote.title,
            'brief': quote.description,
            'status': 'approved',
            'total_price': quote.budget or 0,
            'client': quote.client,
            'service': quote.service
        }
        
        project = Project.objects.create(**project_data)
        
        # Actualizar cotización
        quote.status = 'approved'
        quote.approved_by = request.user
        quote.approved_at = timezone.now()
        quote.linked_project = project
        quote.save()
        
        return Response({
            'message': 'Cotización aprobada y proyecto creado',
            'project_id': project.id,
            'quote': QuoteRequestSerializer(quote).data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rechazar cotización"""
        quote = self.get_object()
        
        if quote.status != 'submitted':
            return Response({'detail': 'Solo se pueden rechazar cotizaciones en estado submitted'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        rejected_reason = request.data.get('rejected_reason', 'Sin motivo especificado')
        
        quote.status = 'rejected'
        quote.rejected_reason = rejected_reason
        quote.save()
        
        return Response({
            'message': 'Cotización rechazada',
            'quote': QuoteRequestSerializer(quote).data
        })


@method_decorator(csrf_exempt, name='dispatch')
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'is_admin') and (user.is_admin() if callable(user.is_admin) else user.is_admin):
            # Admin puede ver todos los proyectos
            return Project.objects.all().order_by('-created_at')
        elif hasattr(user, 'is_designer') and (user.is_designer() if callable(user.is_designer) else user.is_designer):
            # Diseñador ve solo los asignados
            return Project.objects.filter(assigned_to=user).order_by('-created_at')
        else:
            # Cliente ve solo los suyos
            return Project.objects.filter(client=user).order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]

    @action(detail=True, methods=['post'])
    def assign_designer(self, request, pk=None):
        """Asignar diseñador a proyecto"""
        project = self.get_object()
        designer_id = request.data.get('designer_id')
        
        if not designer_id:
            return Response({'detail': 'designer_id es requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            designer = User.objects.get(id=designer_id)
            if not (hasattr(designer, 'is_designer') and designer.is_designer):
                return Response({'detail': 'El usuario seleccionado no es un diseñador'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Diseñador no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        project.assigned_to = designer
        project.status = 'in_progress'
        project.save()
        
        return Response({
            'message': f'Diseñador {designer.username} asignado al proyecto',
            'project': ProjectSerializer(project).data
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_completed_by_designer(self, request, pk=None):
        """Permite al diseñador marcar el proyecto como completado (requiere confirmación del admin)"""
        project = self.get_object()
        user = request.user
        
        if not (hasattr(user, 'is_designer') and user.is_designer and project.assigned_to == user):
            return Response({'detail': 'Solo el diseñador asignado puede marcar como completado'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        if project.status != 'in_progress':
            return Response({'detail': 'Solo proyectos en progreso pueden ser marcados como completados'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        project.status = 'pending_completion_confirmation'
        project.save()
        
        return Response({
            'message': 'Proyecto marcado como completado. Esperando confirmación del administrador.',
            'project': ProjectSerializer(project).data
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def confirm_completion(self, request, pk=None):
        """Permite al admin confirmar que un proyecto está completado"""
        project = self.get_object()
        
        if project.status != 'pending_completion_confirmation':
            return Response({'detail': 'Solo proyectos pendientes de confirmación pueden ser confirmados'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        project.status = 'completed'
        project.save()
        
        return Response({
            'message': 'Proyecto confirmado como completado exitosamente.',
            'project': ProjectSerializer(project).data
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def mark_completed_by_admin(self, request, pk=None):
        """Permite al admin marcar directamente un proyecto como completado"""
        project = self.get_object()
        
        if project.status not in ['in_progress', 'pending_completion_confirmation']:
            return Response({'detail': 'Solo proyectos en progreso o pendientes de confirmación pueden ser marcados como completados'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        project.status = 'completed'
        project.save()
        
        return Response({
            'message': 'Proyecto marcado como completado por el administrador.',
            'project': ProjectSerializer(project).data
        })


@method_decorator(csrf_exempt, name='dispatch')
class ProjectMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMessageSerializer
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return ProjectMessage.objects.filter(project_id=project_id).order_by('created_at')
    
    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsProjectParticipant()]
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(sender=self.request.user, project=project)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUserCustom()]

    @action(detail=False, methods=['post'])
    def simulate(self, request):
        """Simular pago de proyecto"""
        project_id = request.data.get('project_id')
        amount = request.data.get('amount')
        
        if not project_id or not amount:
            return Response({'detail': 'project_id y amount son requeridos'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'detail': 'Proyecto no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Crear pago simulado
        payment = Payment.objects.create(
            project=project,
            amount=amount,
            status='completed',
            is_simulated=True,
            cardholder_name=request.data.get('cardholder_name', ''),
            card_last4=request.data.get('card_last4', '')
        )
        
        # Actualizar proyecto
        project.paid_amount = amount
        project.status = 'in_progress'
        project.save()
        
        return Response({
            'message': 'Pago simulado exitoso',
            'payment': PaymentSerializer(payment).data,
            'project': ProjectSerializer(project).data
        })