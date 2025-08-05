from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Users
from .serializer import (
    UserRegisterSerializer,
    UserCreateByAdminSerializer,
    BranchCreateByAdminSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)
from .permissions import IsAdminUserCustom


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    tags=['authentication'],
    summary='Registro de usuario',
    description='Permite a un usuario crear su propia cuenta en el sistema',
    request=UserRegisterSerializer,
    responses={
        201: UserDetailSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    examples=[
        OpenApiExample(
            'Registro exitoso',
            value={
                'username': 'nuevo_usuario',
                'email': 'usuario@example.com',
                'password': 'Password123!',
                'password2': 'Password123!',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'phone': '123456789',
                'address': 'Calle Principal 123',
                'roles': 'cliente'
            },
            request_only=True,
        ),
    ],
)
class UserRegisterView(viewsets.ModelViewSet):
    """Vista para registro de usuario creando su propia cuenta"""
    serializer_class = UserRegisterSerializer
    queryset = Users.objects.all()
    http_method_names = ['post']  # Solo permitimos POST para registrar
    permission_classes = [AllowAny]


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    tags=['authentication'],
    summary='Inicio de sesión',
    description='Permite a un usuario iniciar sesión usando username o email',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'identifier': {'type': 'string', 'description': 'Username o email del usuario'},
                'password': {'type': 'string', 'description': 'Contraseña del usuario'},
            },
            'required': ['identifier', 'password'],
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'user': UserDetailSerializer,
                'session_id': {'type': 'string'},
            }
        },
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        500: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    },
    examples=[
        OpenApiExample(
            'Login exitoso',
            value={
                'identifier': 'usuario@example.com',
                'password': 'Password123!'
            },
            request_only=True,
        ),
    ],
)
class LoginView(APIView):
    """Vista de login por username o email con manejo de sesiones"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            identifier = request.data.get("identifier")
            password = request.data.get("password")

            if not identifier or not password:
                return Response(
                    {"error": "Se requiere 'identifier' y 'password'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Buscar usuario por username o email
            user_obj = None
            try:
                user_obj = Users.objects.get(username=identifier)
            except Users.DoesNotExist:
                try:
                    user_obj = Users.objects.get(email=identifier)
                except Users.DoesNotExist:
                    return Response(
                        {"error": "Usuario no encontrado"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Autenticar usuario
            user = authenticate(request, username=user_obj.username, password=password)

            if user and user.is_active:
                login(request, user)
                
                # Serializar datos del usuario para la respuesta
                serializer = UserDetailSerializer(user)
                
                return Response({
                    "message": "Login exitoso",
                    "user": serializer.data,
                    "session_id": request.session.session_key,
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Credenciales incorrectas o usuario inactivo"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {"error": f"Error en el login: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    tags=['authentication'],
    summary='Cerrar sesión',
    description='Cierra la sesión del usuario actual',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'message': {'type': 'string'},
                'session_cleared': {'type': 'boolean'},
            }
        },
    },
)
class LogoutView(APIView):
    """Vista para cerrar sesión"""
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({
            "message": "Logout exitoso",
            "session_cleared": True
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['users'],
    summary='Obtener perfil de usuario',
    description='Obtiene la información del perfil del usuario autenticado',
    responses={
        200: UserDetailSerializer,
        401: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
    },
)
class UserProfileView(APIView):
    """Vista para obtener y actualizar el perfil del usuario"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener perfil del usuario actual"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Actualizar perfil del usuario actual"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Perfil actualizado correctamente",
                "user": UserDetailSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionStatusView(APIView):
    """Vista para verificar el estado de la sesión"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserDetailSerializer(request.user)
            return Response({
                "authenticated": True,
                "user": serializer.data,
                "session_id": request.session.session_key,
            })
        else:
            return Response({
                "authenticated": False,
                "message": "Usuario no autenticado"
            })


class ProtectedView(APIView):
    """Vista protegida para probar autenticación"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f'¡Hola, {request.user.username}! Estás autenticado.',
            'user_id': request.user.id,
            'email': request.user.email,
            'roles': request.user.roles,
            'session_id': request.session.session_key,
        })


@extend_schema(
    tags=['users'],
    summary='Crear usuario (Admin)',
    description='Permite a un administrador crear nuevos usuarios en el sistema',
    request=UserCreateByAdminSerializer,
    responses={
        201: UserDetailSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        403: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
    },
)
class CreateUserByAdminView(generics.CreateAPIView):
    """Vista para que un admin cree usuarios"""
    serializer_class = UserCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_admin:
            raise permissions.PermissionDenied("No tienes permiso para crear usuarios.")
        serializer.save()


@extend_schema(
    tags=['branches'],
    summary='Crear sucursal (Admin)',
    description='Permite a un administrador crear nuevas sucursales',
    request=BranchCreateByAdminSerializer,
    responses={
        201: BranchCreateByAdminSerializer,
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        403: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
    },
)
class CreateBranchByAdminView(generics.CreateAPIView):
    """Vista para que un admin cree sucursales"""
    serializer_class = BranchCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_admin:
            raise permissions.PermissionDenied("Solo los administradores pueden crear sucursales.")
        serializer.save()


@method_decorator(csrf_exempt, name='dispatch')
class TestView(APIView):
    """Vista de prueba para verificar que todo funciona"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            "message": "¡API funcionando correctamente!",
            "session_id": request.session.session_key,
            "authenticated": request.user.is_authenticated
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({
            "message": "POST funcionando correctamente!",
            "data_received": request.data
        }, status=status.HTTP_200_OK)
