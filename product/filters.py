import django_filters
from product.models import *
from django import forms


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', )
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple, )
