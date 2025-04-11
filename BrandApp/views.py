from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *

class UserSerializerView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProductSerializerView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class CategorySerializerView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class OrderSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetails.objects.all()

class ShoppCartSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartSerializer
    queryset = ShoppCart.objects.all()

class ShoppCartDetailsSerializerView(viewsets.ModelViewSet):
    serializer_class = ShoppCartDetailsSerializer
    queryset = ShoppCartDetails.objects.all()

class ReviewsSerializerView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()

