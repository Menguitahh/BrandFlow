from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
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
from .permissions import IsAdminUserCustom, IsAdmin


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

    def create(self, request, *args, **kwargs):
        # Usamos el serializer de registro pero respondemos con UserDetailSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Login automático después del registro para establecer sesión
        login(request, user)
        
        detail = UserDetailSerializer(user, context={'request': request})
        headers = self.get_success_headers(detail.data)
        
        return Response({
            "message": "Usuario registrado e iniciado sesión exitosamente",
            "user": detail.data,
            "session_id": request.session.session_key,
        }, status=status.HTTP_201_CREATED, headers=headers)


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


@extend_schema(
    tags=['admin'],
    summary='Listar todos los usuarios (Admin)',
    description='Permite a un admin ver todos los usuarios con filtros por rol',
    parameters=[
        OpenApiParameter(name='role', description='Filtrar por rol', required=False, type=str),
        OpenApiParameter(name='search', description='Buscar por nombre o email', required=False, type=str),
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'users': {
                    'type': 'array',
                    'items': UserDetailSerializer
                },
                'total': {'type': 'integer'},
                'filters': {'type': 'object'}
            }
        }
    }
)
class AdminUserListView(APIView):
    """Vista para que admin liste todos los usuarios con filtros"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        # Obtener parámetros de filtro
        role_filter = request.query_params.get('role')
        search_query = request.query_params.get('search', '')
        
        # Query base
        queryset = Users.objects.all().order_by('-date_joined')
        
        # Aplicar filtros
        if role_filter:
            queryset = queryset.filter(roles=role_filter)
        
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        
        # Serializar usuarios
        serializer = UserDetailSerializer(queryset, many=True)
        
        return Response({
            'users': serializer.data,
            'total': queryset.count(),
            'filters': {
                'role': role_filter,
                'search': search_query
            }
        })


@extend_schema(
    tags=['admin'],
    summary='Listar diseñadores disponibles (Admin)',
    description='Obtiene lista de usuarios con rol diseñador para asignación de proyectos',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'designers': {
                    'type': 'array',
                    'items': UserDetailSerializer
                },
                'total': {'type': 'integer'}
            }
        }
    }
)
class AdminDesignersListView(APIView):
    """Vista para que admin obtenga lista de diseñadores disponibles"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        # Obtener solo usuarios con rol diseñador
        designers = Users.objects.filter(roles='diseñador').order_by('username')
        serializer = UserDetailSerializer(designers, many=True)
        
        return Response({
            'designers': serializer.data,
            'total': designers.count()
        })


@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    tags=['admin'],
    summary='Cambiar rol de usuario (Admin)',
    description='Permite a un admin asignar rol a un usuario: diseñador, cliente, gerente, vendedor o admin',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer'},
                'role': {'type': 'string', 'enum': ['diseñador', 'cliente', 'gerente', 'vendedor', 'admin']},
            },
            'required': ['user_id', 'role']
        }
    },
)
class AdminSetRoleView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        user_id = request.data.get('user_id')
        role = request.data.get('role')
        if not user_id or not role:
            return Response({"detail": "user_id y role son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        if role not in ['diseñador', 'cliente', 'gerente', 'vendedor', 'admin']:
            return Response({"detail": "Rol inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Evitar que un no-admin cambie su propio rol (ya cubierto por permiso),
        # adicionalmente impedir auto-escalado si no fuera admin
        if target.id == request.user.id and not (hasattr(request.user, 'is_admin') and request.user.is_admin()):
            return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

        target.roles = role
        target.save()
        return Response(UserDetailSerializer(target).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['users'],
    summary='Obtener información básica de usuarios',
    description='Permite a cualquier usuario autenticado obtener información básica (nombre, username, rol) de usuarios específicos',
    parameters=[
        OpenApiParameter(
            name='user_ids',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='IDs de usuarios separados por comas (ej: 1,2,3)',
            required=True
        )
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'users': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'username': {'type': 'string'},
                            'role': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
)
class GetUsersBasicInfoView(APIView):
    """Endpoint para obtener información básica de usuarios específicos"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_ids_str = request.query_params.get('user_ids')
        if not user_ids_str:
            return Response({"detail": "user_ids es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parsear los IDs
            user_ids = [int(id.strip()) for id in user_ids_str.split(',') if id.strip()]
        except ValueError:
            return Response({"detail": "user_ids debe contener solo números separados por comas"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener usuarios
        users = Users.objects.filter(id__in=user_ids).values('id', 'first_name', 'last_name', 'username', 'roles')
        
        # Convertir a formato de respuesta
        users_data = []
        for user in users:
            users_data.append({
                'id': user['id'],
                'first_name': user['first_name'] or '',
                'last_name': user['last_name'] or '',
                'username': user['username'],
                'role': user['roles']
            })

        return Response({"users": users_data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['users'],
    summary='Verificar disponibilidad de nombre de usuario',
    description='Verifica si un nombre de usuario está disponible para registro',
    parameters=[
        OpenApiParameter(
            name='username',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Nombre de usuario a verificar',
            required=True
        )
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'available': {'type': 'boolean'},
                'username': {'type': 'string'}
            }
        }
    }
)
class CheckUsernameAvailabilityView(APIView):
    """Endpoint para verificar disponibilidad de username"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({"detail": "username es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el username ya existe
        exists = Users.objects.filter(username__iexact=username).exists()
        
        return Response({
            "available": not exists,
            "username": username
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['users'],
    summary='Verificar disponibilidad de email',
    description='Verifica si un email está disponible para registro',
    parameters=[
        OpenApiParameter(
            name='email',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Email a verificar',
            required=True
        )
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'available': {'type': 'boolean'},
                'email': {'type': 'string'}
            }
        }
    }
)
class CheckEmailAvailabilityView(APIView):
    """Endpoint para verificar disponibilidad de email"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"detail": "email es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el email ya existe
        exists = Users.objects.filter(email__iexact=email).exists()
        
        return Response({
            "available": not exists,
            "email": email
        }, status=status.HTTP_200_OK)


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
