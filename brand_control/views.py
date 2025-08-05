from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *
from rest_framework import permissions, viewsets
from user_control.permissions import IsAdminUserCustom

# class UserSerializerView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()


class ProductSerializerView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Cambiado para permitir usuarios autenticados


class CategorySerializerView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class OrderSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class OrderDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()

class ShoppCartSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartSerializer
    queryset = ShoppCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class ShoppCartDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartDetailsSerializer
    queryset = ShoppCartDetails.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Agregado para usuarios autenticados

class ReviewsSerializerView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()

