from django.contrib import admin
from django.contrib.admin import register
from .models import *


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ('user', 'product', 'variant', 'size', 'quantity')


@register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'paid', 'f_name', 'l_name', 'address', 'get_price']
    inlines = [ItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'active', 'start', 'end', 'discount', ]


admin.site.register(ItemOrder)
admin.site.register(Coupon, CouponAdmin)
