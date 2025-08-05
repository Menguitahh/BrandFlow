from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.contrib.auth import get_user
import json


class SessionMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para manejar sesiones y autenticación
    """
    
    def process_request(self, request):
        """Procesa la request antes de que llegue a la vista"""
        # Asegurar que la sesión esté creada
        if not request.session.session_key:
            request.session.create()
        
        # Obtener el usuario autenticado
        request.user = get_user(request)
        
        return None
    
    def process_response(self, request, response):
        """Procesa la response antes de enviarla al cliente"""
        
        # Si es una respuesta JSON y el usuario está autenticado, agregar información de sesión
        if hasattr(response, 'content_type') and response.content_type and 'application/json' in response.content_type:
            try:
                content = json.loads(response.content.decode('utf-8'))
                if request.user.is_authenticated:
                    content['session_info'] = {
                        'session_id': request.session.session_key,
                        'user_id': request.user.id,
                        'authenticated': True
                    }
                else:
                    content['session_info'] = {
                        'session_id': request.session.session_key,
                        'authenticated': False
                    }
                response.content = json.dumps(content, ensure_ascii=False).encode('utf-8')
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        
        # Configurar headers de seguridad para cookies
        if hasattr(response, 'cookies'):
            for cookie in response.cookies.values():
                cookie['httponly'] = True
                cookie['samesite'] = 'Lax'
        
        return response
    
    def process_exception(self, request, exception):
        """Maneja excepciones durante el procesamiento de la request"""
        if isinstance(exception, Exception):
            return JsonResponse({
                'error': 'Error interno del servidor',
                'message': str(exception),
                'session_id': request.session.session_key if hasattr(request, 'session') else None
            }, status=500)
        return None


class CSRFMiddleware(MiddlewareMixin):
    """
    Middleware para manejar CSRF de manera más flexible en desarrollo
    """
    
    def process_request(self, request):
        """Procesa la request para CSRF"""
        # Para desarrollo, permitir requests sin CSRF en ciertos endpoints
        csrf_exempt_paths = [
            '/api/user/test/',
            '/api/user/register/',
            '/api/user/login/',
            '/api/user/logout/',
        ]
        
        for path in csrf_exempt_paths:
            if request.path.startswith(path):
                setattr(request, '_dont_enforce_csrf_checks', True)
                break
        
        return None 