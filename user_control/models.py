from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Users(AbstractUser):
    # iduser = models.AutoField(primary_key=True)  #! los PK esperar a confirmar si se necesita o no    
    # password = models.CharField(max_length=100,)
    # email = models.EmailField(max_length=100,)
    phone = models.CharField(max_length=15,)
    address  = models.CharField(max_length=100,)
    # username = models.CharField(max_length=100,)
    roles = models.CharField(max_length=50, default='cliente')  # o el valor por defecto que quieras
    def __str__(self):
        return self.username
    
