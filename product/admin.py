from django.contrib import admin
from .models import Products, variants, Color, Size
from django.contrib.admin import register


# Register your models here.

class product_variants(admin.TabularInline):
    model = variants
    extra = 2


@register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'image', 'available', 'description', 'option_status', 'id','discount' ]
    list_filter = ['available']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('color','size')
    inlines = (product_variants,)


@register(Color)
class colorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@register(variants)
class variants(admin.ModelAdmin):
    list_display = ['name', 'product_variant', 'color_variant', 'unit_price', 'size_variant', 'id','discount']
    list_filter = ['name', ]
