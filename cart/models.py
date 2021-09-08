from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Products, variants
from django import forms

User = get_user_model()


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant = models.ForeignKey(variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('تعداد'))


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
