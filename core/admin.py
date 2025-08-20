from django.contrib import admin

# Register your models here.

from .models import Empresa, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
	list_display = ("nombre", "direccion", "telefono", "email", "created_at")
	search_fields = ("nombre", "email")

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	list_display = ("username", "email", "empresa", "rol", "is_active", "is_staff")
	list_filter = ("empresa", "rol", "is_active", "is_staff")
	fieldsets = UserAdmin.fieldsets + (
		("Información de empresa y rol", {"fields": ("empresa", "rol")}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		("Información de empresa y rol", {"fields": ("empresa", "rol")}),
	)
