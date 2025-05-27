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
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]


class CategorySerializerView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class OrderSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()

class Shopp_CartSerializerView(viewsets.ModelViewSet):
    serializer_class = Shopp_CartSerializer
    queryset = Shopp_Cart.objects.all()

class Shopp_Cart_DetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = Shopp_Cart_DetailsSerializer
    queryset = Shopp_Cart_Details.objects.all()

class ReviewsSerializerView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()
    


