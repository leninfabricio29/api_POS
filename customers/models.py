# customers/models.py
from django.db import models
from core.models import TimeStampedModel

class Customer(TimeStampedModel):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    doc_id = models.CharField(max_length=30, blank=True, null=True)  # cédula/RUC

    def __str__(self):
        return self.name