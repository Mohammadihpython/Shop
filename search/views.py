from django.db import models
from django.db.models import Q
from django.db.models.functions import Greatest
from django.shortcuts import render

# from django.db.models import Q
# from django.apps import apps
from product.models import variants, Products
from django.contrib.postgres.search import TrigramSimilarity
from django import forms

class Search(forms.Form):
    search = forms.CharField()


def DoSearch(request):
    products = Products.objects.all()
    s_form = Search()
    if 'search' in request.GET:
        s_form = Search(request.GET)
        if s_form.is_valid():
            res = s_form.cleaned_data['search']
            products = products.filter(Q(name__icontains = res))

    return render(request, 'mobile/result.html', {'products': products, 's_form': s_form})
