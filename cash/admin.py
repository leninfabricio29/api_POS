from django.contrib import admin

# Register your models here.

from .models import CashMovement, CashSession

admin.site.register(CashSession)
admin.site.register(CashMovement)
