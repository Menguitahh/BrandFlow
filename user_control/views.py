# from django.shortcuts import render
# from rest_framework import viewsets
# from .serializer import *
# from .models import User
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import User
from .serializer import UserSerializer

# Create your views here.
class UserSerializerView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Usar el sistema de autenticación de Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si las credenciales son válidas, iniciar sesión
            login(request, user)
            return Response({
                "message": "Login exitoso",
                "username": user.username,
                "role": user.roles
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    # Logout simbólico, ya que no estás usando sesiones reales
    def post(self, request):
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)