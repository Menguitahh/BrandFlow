from django.db import models
from django.utils import timezone
from django.conf import settings
from user_control.models import Users

class Product(models.Model):
    
    name = models.CharField(max_length=100,)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #image = models.ImageField(upload_to='products/')
    type = models.CharField(max_length=100,)
    stock = models.IntegerField()
    url_download = models.URLField(max_length=200,) # A confirmar longitud porque siempre varia
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')


class Category(models.Model):
    name = models.CharField(max_length=100,)
    description = models.TextField()

class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100,)
    user = models.ForeignKey('user_control.Users', on_delete=models.CASCADE, null=True, blank=True)
    

class OrderDetails(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Shopp_Cart(models.Model):
    user = models.ForeignKey('user_control.Users', on_delete=models.CASCADE)



class Shopp_Cart_Details(models.Model):
    
    Shopp_Cart = models.ForeignKey('Shopp_Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Reviews(models.Model):
    user = models.ForeignKey('user_control.Users', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    

class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    method = models.CharField(max_length=100,)
    status = models.CharField(max_length=100,)
    date_payment = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    

class Branch(models.Model):
    pass
