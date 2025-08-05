from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Users
from .serializer import (
    UserRegisterSerializer,
    UserCreateByAdminSerializer,
    BranchCreateByAdminSerializer,
)
from .permissions import IsAdminUserCustom


class UserRegisterView(viewsets.ModelViewSet):
    """Vista para registro de usuario creando su propia empresa"""
    serializer_class = UserRegisterSerializer
    queryset = Users.objects.all()
    http_method_names = ['post']  # Solo permitimos POST para registrar


class LoginView(APIView):
    """Vista de login por username o email"""
    def post(self, request):
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Se requiere 'identifier' y 'password'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = Users.objects.get(username=identifier)
        except Users.DoesNotExist:
            try:
                user_obj = Users.objects.get(email=identifier)
            except Users.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            return Response({
                "email": user.email,
                "roles": user.roles,
            }, status=status.HTTP_200_OK)

        return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Vista para cerrar sesión"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)


class ProtectedView(APIView):
    """Vista protegida con JWT para probar autenticación"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f'¡Hola, {request.user.username}! Estás autenticado con JWT.',
            'user_id': request.user.id,
            'email': request.user.email,
            'roles': request.user.roles
        })


class CreateUserByAdminView(generics.CreateAPIView):
    """Vista para que un admin cree usuarios"""
    serializer_class = UserCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        user = self.request.user
        if user.roles != 'admin':
            raise permissions.PermissionDenied("No tienes permiso para crear usuarios.")
        serializer.save(company=user.company)


class CreateBranchByAdminView(generics.CreateAPIView):
    """Vista para que un admin cree sucursales"""
    serializer_class = BranchCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        user = self.request.user
        if user.roles != 'admin':
            raise permissions.PermissionDenied("Solo los administradores pueden crear sucursales.")
        serializer.save()
