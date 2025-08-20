# cash/models.py
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class CashSession(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    opened_at = models.DateTimeField()
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closed_at = models.DateTimeField(blank=True, null=True)
    closing_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    @property
    def is_open(self):
        return self.closed_at is None

    def __str__(self):
        return f"Caja {self.id} ({'Abierta' if self.is_open else 'Cerrada'})"

class CashMovement(TimeStampedModel):
    class Type(models.TextChoices):
        INFLOW = 'INFLOW', 'Ingreso'
        OUTFLOW = 'OUTFLOW', 'Egreso'

    session = models.ForeignKey(CashSession, on_delete=models.CASCADE, related_name='movements')
    type = models.CharField(max_length=7, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)