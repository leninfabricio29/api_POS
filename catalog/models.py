# catalog/models.py
from django.db import models
from core.models import TimeStampedModel


from core.models import Empresa

class Category(TimeStampedModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    # Opcional: receta/mermas/impresión por estación (cocina/bar)

    def __str__(self):
        return self.name