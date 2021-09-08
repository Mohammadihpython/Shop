from django.db import models
from django.db.models import Q
from django.db.models.functions import Greatest
from django.shortcuts import render

# from django.db.models import Q
# from django.apps import apps
from product.models import variants, Products
from django.contrib.postgres.search import TrigramSimilarity
from django import forms


# class SearchViewForm(forms.Form):
#     template_name = 'mobile/result_search.html'
#     paginate_by = 4
#
#     def get_queryset(self):
#         request = self.request
#         query = request.GET.get('q', '')
#         search_models = [apps.get_models(include_auto_created=True, )]
#         search_result = []
#         for model in search_models:
#             # noinspection PyProtectedMember
#             fields = [i for i in model.fields if isinstance(i, models.CharField)]
#             search_queries = [Q(**{i.name + "__contain": "search_query"}) for i in fields]
#             q_object = Q()
#             for query in search_queries:
#                 q_object = q_object | query
#
#             results = model.objects.filter(q_object)
#             search_result.append(results)
#
#         return render(request, 'mobile/result_search.html', context=search_result)
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
