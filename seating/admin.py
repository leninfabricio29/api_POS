from django.contrib import admin

# Register your models here.
from .models import Area, Table

admin.site.register(Area)
admin.site.register(Table)
