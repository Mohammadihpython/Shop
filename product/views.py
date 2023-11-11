from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
# Create your views here.
from django.template.response import TemplateResponse

from search.views import DoSearch
from .filters import ProductFilter
from .models import Products, variants
from comment.models import CommentForm, Comment
from cart.models import CartForm


def ProductView(request):
    item = Products.objects.order_by('-published')
    filters = ProductFilter(request.GET, queryset=item)
    item = filters.qs

    return render(request, 'mobile/blog.html', {'items': item, 'filters': filters})


def ProductDetailView(request, pk):
    product = Products.objects.get(id=pk)
    comment_form = CommentForm()
    comment = Comment.objects.filter(product_id=pk)
    cart_form = CartForm()
    if Products.option_status == 'None':
        return render(request, 'mobile/blog_detail.html', {'product': product, 'comment_form': comment_form,
                                                          'comment': comment, 'cart_form': cart_form})
    var_id = None
    var = None
    variant =None
    if request.method == 'POST':
        variant = variants.objects.filter(product_variant_id=pk)
        var_id = request.POST.get('select')
        var = variants.objects.get(id=var_id)
    elif request.method == 'GET':
        variant = variants.objects.filter(product_variant_id=pk)
        var = variants.objects.get(id=variant[0].id)

    args = {'product': product, 'var': var, 'variant': variant, 'comment_form': comment_form,
            'comment': comment, 'cart_form': cart_form}
    return render(request, 'mobile/blog_detail.html', args)




@login_required
def favourite_list(request):
    new = Products.objects.filter(favourites=request.user)
    return render(request,
                  'account/favourite.html',
                  {'new': new})


@login_required
def favourite_add(request, id):
    post = get_object_or_404(Products, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
