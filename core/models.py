from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

from django.contrib.auth.models import AbstractUser

class Empresa(TimeStampedModel):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    ADMINISTRADOR = 'ADMIN'
    EMPLEADO = 'EMPLOYEE'
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (EMPLEADO, 'Empleado'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    rol = models.CharField(max_length=20, choices=ROLES, default=EMPLEADO)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

AUTH_USER_MODEL = 'core.CustomUser'