"""
Middleware personalizado para deshabilitar CSRF en APIs REST
"""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware para deshabilitar CSRF en rutas de API
    """
    
    def process_request(self, request):
        # Deshabilitar CSRF para todas las rutas que empiecen con /api/
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None

