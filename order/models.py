from django.db import models
from django.contrib.auth import get_user_model
from product.models import *
from django.forms import ModelForm

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField()
    f_name = models.CharField(max_length=250)
    l_name = models.CharField(max_length=250)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.f_name

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', )
    product = models.ForeignKey(Products, on_delete=models.CASCADE,verbose_name='product' )
    variant = models.ForeignKey(variants, on_delete=models.CASCADE, null=True, blank=True,verbose_name='variant')
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username

    def size(self):
        return self.variant.size_variant.name

    def price(self):
        if self.product.option_status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.PositiveIntegerField()


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'f_name', 'l_name', 'address']
