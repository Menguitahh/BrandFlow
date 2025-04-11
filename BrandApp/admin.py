from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(ShoppCart)
admin.site.register(ShoppCartDetails)
admin.site.register(Reviews)
# admin.site.register(Payment) #! este va dependiendo los metodos de pago
# admin.site.register(method_payment) #! este va dependiendo los metodos de pago
#ajustar
# Register your models here.
