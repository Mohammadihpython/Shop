from django.shortcuts import render, redirect
from product.models import *
from .models import Cart, CartForm
from django.contrib.auth.decorators import login_required
from order.models import OrderForm


# Create your views here.


def CartView(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    order_form = OrderForm()
    total = 0
    for p in cart:
        if p.product.option_status != 'None':
            total += p.variant.unit_price
        else:
            total += p.product.price * p.product.discount / 100 * p.quantity
    return render(request, 'mobile/cart.html', {'cart': cart, 'total': total , 'order_form': order_form})


@login_required(login_url='account:login')
def Add_Cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Products.objects.get(id=id)

    if product.option_status != 'None':
        var_id = request.POST.get('var_id')
        data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('var_id')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.option_status != 'None':
                    obj = Cart.objects.get(user_id=request.user.id, variant_id=var_id)
                else:
                    obj = Cart.objects.get(user_id=request.user.id, product_id=id)
                obj.quantity += info
                obj.save()
            else:
                Cart.objects.create(user_id=request.user.id, product_id=id, variant_id=var_id, quantity=info)

    return redirect(url)


@login_required(login_url='account:login')
def Del_Cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)
