from django.db import models
from django.utils import timezone
from django.conf import settings
from user_control.models import Users


# Create your models here.
# class User(models.Model):
#     iduser = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
#     password = models.CharField(max_length=100,)
#     email = models.EmailField(max_length=100,)
#     phone = models.CharField(max_length=15,)
#     addres = models.CharField(max_length=100,)
#     username = models.CharField(max_length=100,)
#     roles = models.CharField(max_length=50, default='cliente')  # o el valor por defecto que quieras
#     def __str__(self):
#         return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    url_download = models.URLField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=100, default='General')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, db_column='category_id')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def update_stock(self, quantity, operation='decrease'):
        """Actualiza el stock del producto"""
        if operation == 'decrease':
            if self.stock >= quantity:
                self.stock -= quantity
                self.save()
                return True
            return False
        elif operation == 'increase':
            self.stock += quantity
            self.save()
            return True
        return False
    
    def has_stock(self, quantity):
        """Verifica si hay stock suficiente"""
        return self.stock >= quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    idorder = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Orden {self.idorder} - {self.user.username}"
    
    def calculate_total(self):
        """Calcula el total de la orden"""
        total = sum(detail.price * detail.quantity for detail in self.orderdetails_set.all())
        self.total = total
        self.save()
        return total
    
    def cancel_order(self):
        """Cancela la orden y restaura el stock"""
        if self.status == 'pending':
            # Restaurar stock de todos los productos
            for detail in self.orderdetails_set.all():
                previous_stock = detail.idproduct.stock
                detail.idproduct.update_stock(detail.quantity, 'increase')
                
                # Crear movimiento de stock para restauración
                StockMovement.objects.create(
                    product=detail.idproduct,
                    movement_type='in',
                    quantity=detail.quantity,
                    previous_stock=previous_stock,
                    new_stock=detail.idproduct.stock,
                    reason=f'Cancelación - Orden {self.idorder}',
                    user=self.user
                )
            self.status = 'cancelled'
            self.save()
            return True
        return False


class OrderDetails(models.Model):
    idorderdetails = models.AutoField(primary_key=True)
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    idorder = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderdetails_set')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Detalle {self.idorderdetails} - {self.idproduct.name}"
    
    def save(self, *args, **kwargs):
        # Si es una nueva instancia, actualizar el stock
        if not self.pk:
            if self.idproduct.has_stock(self.quantity):
                previous_stock = self.idproduct.stock
                self.idproduct.update_stock(self.quantity, 'decrease')
                
                # Crear movimiento de stock
                StockMovement.objects.create(
                    product=self.idproduct,
                    movement_type='out',
                    quantity=self.quantity,
                    previous_stock=previous_stock,
                    new_stock=self.idproduct.stock,
                    reason=f'Venta - Orden {self.idorder.idorder}',
                    user=self.idorder.user
                )
            else:
                raise ValueError("Stock insuficiente")
        super().save(*args, **kwargs)


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
    idshoppcart = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='shopping_carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrito {self.idshoppcart} - {self.user.username}"
    
    def get_total(self):
        """Calcula el total del carrito"""
        return sum(detail.idproduct.price * detail.quantity for detail in self.shoppcartdetails_set.all())
    
    def clear_cart(self):
        """Vacía el carrito"""
        self.shoppcartdetails_set.all().delete()


class ShoppCartDetails(models.Model):
    idshoppcartdetails = models.AutoField(primary_key=True)
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_details')
    idshoppcart = models.ForeignKey(ShoppCart, on_delete=models.CASCADE, related_name='shoppcartdetails_set')
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Carrito {self.idshoppcartdetails} - {self.idproduct.name}"
    
    def save(self, *args, **kwargs):
        # Verificar stock antes de agregar al carrito
        if not self.idproduct.has_stock(self.quantity):
            raise ValueError("Stock insuficiente para agregar al carrito")
        super().save(*args, **kwargs)


class Reviews(models.Model):
    idreviews = models.AutoField(primary_key=True)
    idproduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Review {self.idreviews} - {self.idproduct.name}"


class Branch(models.Model):
    idbranch = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, default='Sin dirección')
    phone = models.CharField(max_length=15)
    company = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='branches', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name


class StockMovement(models.Model):
    """Modelo para rastrear movimientos de stock"""
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
    ]
    
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    reason = models.CharField(max_length=200)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='stock_movements')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity}"
