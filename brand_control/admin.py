from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(ShoppCart)
admin.site.register(ShoppCartDetails)
admin.site.register(Reviews)
