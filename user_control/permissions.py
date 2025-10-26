from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminUserCustom(BasePermission):
    """Permiso personalizado para verificar si el usuario es administrador"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin()
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin()
        )


class IsOwnerOrAdmin(BasePermission):
    """Permiso para que solo el propietario o admin pueda acceder"""
    
    def has_object_permission(self, request, view, obj):
        # Los admins pueden acceder a todo
        if request.user.is_authenticated and (
            getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin()
        ):
            return True
        
        # El propietario puede acceder a sus propios datos
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        
        return False


class IsCompanyMember(BasePermission):
    """Permiso para verificar si el usuario pertenece a la misma empresa"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Los admins pueden acceder a todo
        if getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin():
            return True
        
        # Verificar si pertenece a la misma empresa
        if hasattr(obj, 'company') and obj.company:
            return obj.company == request.user.company
        
        return False
    
    

class IsClientUser(BasePermission):
    """Permiso para verificar si el usuario es cliente"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_client', False) if isinstance(request.user.is_client, bool) else request.user.is_client()
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_client', False) if isinstance(request.user.is_client, bool) else request.user.is_client()
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin()
        )


class IsDesigner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            hasattr(request.user, 'is_designer') and request.user.is_designer()
        )


class IsProjectParticipant(BasePermission):
    """Permite acceso si el usuario participa en el proyecto (cliente o asignado). Se espera que la vista
    defina get_project(obj o id) o que el objeto tenga 'client' y 'assigned_to'."""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        is_admin = getattr(request.user, 'is_admin', False) if isinstance(request.user.is_admin, bool) else request.user.is_admin()
        if is_admin:
            return True
        client = getattr(obj, 'client', None)
        assigned = getattr(obj, 'assigned_to', None)
        return client == request.user or assigned == request.user
