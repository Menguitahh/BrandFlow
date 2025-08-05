from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Users(AbstractUser):
    # Campos adicionales
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    roles = models.CharField(max_length=50, default='cliente', choices=[
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('gerente', 'Gerente'),
    ])
    
    # Campo para relacionar usuarios con empresas (para admins)
    company = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    
    # Campos de auditoría (opcionales para evitar problemas de migración)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.roles})"
    
    @property
    def is_admin(self):
        return self.roles == 'admin'
    
    @property
    def is_client(self):
        return self.roles == 'cliente'
    
    @property
    def is_seller(self):
        return self.roles == 'vendedor'
    
    @property
    def is_manager(self):
        return self.roles == 'gerente'
    
