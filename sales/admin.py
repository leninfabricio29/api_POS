from django.contrib import admin

# Register your models here.
from .models import Sale, Payment

admin.site.register(Sale)
admin.site.register(Payment)
