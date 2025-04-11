from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('idproduct', 'name', 'description', 'price', 'image', 'stock', 'url_download', 'category')
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'



# class UserSerializer(serializers.ModelSerializer):   #! Asignado a los metodos de pago si es que es necesario
#     class Meta:
#         model = User
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'



# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
#         fields = '__all__'

class ShoppCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppCart
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class ShoppCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppCartDetails
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'

