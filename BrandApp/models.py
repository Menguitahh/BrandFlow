from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    iduser = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
    password = models.CharField(max_length=100,)
    email = models.EmailField(max_length=100,)
    phone = models.CharField(max_length=15,)
    addres = models.CharField(max_length=100,)
    username = models.CharField(max_length=100,)
    roles = models.CharField(max_length=50, default='cliente')  # o el valor por defecto que quieras
    def __str__(self):
        return self.username


class Product(models.Model):
    idproduct = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
    name = models.CharField(max_length=100,)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    url_download = models.URLField(max_length=200,) # A confirmar longitud porque siempre varia
    category = models.CharField(max_length=100,)
    def __str__(self):
        return self.name

class Category(models.Model):
    idcategory = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
    name = models.CharField(max_length=100,)
    description = models.TextField()
    def __str__(self):
        return self.name

class Order(models.Model):
    idorder = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no
    date = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100,)
    iduser = models.ForeignKey(User, on_delete=models.CASCADE) #! arreglar/asociar con usuario 
    def __str__(self):
        return str(self.idorder)
    

class OrderDetails(models.Model):
    idorderdetails = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE) #! arreglar/asociar con producto 
    idorder = models.ForeignKey(Order, on_delete=models.CASCADE) #! arreglar/asociar con orden
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    def __str__(self):
        return str(self.idorderdetails)

# class payment_methods (
#     ('credit_card', 'Credit Card'),      #! Consultar como se deberia agregar los metodos de pago
#     ('debit_card', 'Debit Card'),
#     ('paypal', 'PayPal'),
#     ('bank_transfer', 'Bank Transfer'),
#     ('cash_on_delivery', 'Cash on Delivery'),
#     ('crypto', 'Crypto'),
# )
# class Payment(models.Model):                  #! este va dependiendo los metodos de pago
#     idpayment = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no   
#     date = models.DateField(default=timezone.now)
#     method = models.CharField(max_length=20, choices=payment_methods)
#     status = models.CharField(max_length=100,)
#     idorder = models.ForeignKey(Order, on_delete=models.CASCADE) #! arreglar/asociar con orden 
#     def __str__(self):
#         return str(self.idpayment)

class ShoppCart(models.Model):
    idshoppcart = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no 
    iduser = models.ForeignKey(User, on_delete=models.CASCADE) #! arreglar/asociar con usuario 
    def __str__(self):
        return str(self.idshoppcart)


class ShoppCartDetails(models.Model):
    idshoppcartdetails = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no 
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE) #! arreglar/asociar con producto 
    idshoppcart = models.ForeignKey(ShoppCart, on_delete=models.CASCADE) #! arreglar/asociar con carrito de compras 
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.idshoppcartdetails)


class Reviews(models.Model):
    idreviews = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no 
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE) #! arreglar/asociar con producto 
    iduser = models.ForeignKey(User, on_delete=models.CASCADE) #! arreglar/asociar con usuario 
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.idreviews)