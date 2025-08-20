# sales/models.py
from django.db import models
from core.models import TimeStampedModel
from orders.models import Order

from core.models import Empresa

class Sale(TimeStampedModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ventas')
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='sale')
    customer_name = models.CharField(max_length=150, blank=True, null=True)  # venta rápida sin registrar
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.total}"

class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = 'CASH', 'Efectivo'
        CARD = 'CARD', 'Tarjeta'
        TRANSFER = 'TRANSFER', 'Transferencia'

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=10, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)  # num. voucher

    def __str__(self):
        return f"{self.method} {self.amount}"