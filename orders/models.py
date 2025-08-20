# orders/models.py
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from seating.models import Table
from customers.models import Customer
from catalog.models import Product

from core.models import Empresa

class Order(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Abierta'
        SENT = 'SENT', 'Enviada a cocina'
        READY = 'READY', 'Lista'

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='orders')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    notes = models.TextField(blank=True, null=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_status_display()}"

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot del precio
    note = models.CharField(max_length=200, blank=True, null=True)  # sin cebolla, etc.

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product} x{self.quantity}"