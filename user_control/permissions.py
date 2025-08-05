from rest_framework.permissions import BasePermission
from user_control.models import Users
class IsAdminUserCustom(BasePermission):
    """Permiso personalizado para verificar si el usuario es administrador"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(BasePermission):
    """Permiso para que solo el propietario o admin pueda acceder"""
    
    def has_object_permission(self, request, view, obj):
        # Los admins pueden acceder a todo
        if request.user.is_authenticated and request.user.is_admin:
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
        if request.user.is_admin:
            return True
        
        # Verificar si pertenece a la misma empresa
        if hasattr(obj, 'company') and obj.company:
            return obj.company == request.user.company
        
        return False
    
    

class IsClientUser(BasePermission):
    """Permiso para verificar si el usuario es cliente"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_client
