from django.db import models
from core.models import TimeStampedModel


from core.models import Empresa

class Area(TimeStampedModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Table(TimeStampedModel):
    class Status(models.TextChoices):
        FREE = 'FREE', 'Libre'
        BUSY = 'BUSY', 'Ocupada'
        BILL = 'BILL', 'En cuenta'

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tables')
    code = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='tables')
    capacity = models.PositiveIntegerField(default=2)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.FREE)

    def __str__(self):
        return f"{self.code} ({self.area})"