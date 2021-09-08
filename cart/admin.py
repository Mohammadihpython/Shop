from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from .models import Cart


@register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', ]
