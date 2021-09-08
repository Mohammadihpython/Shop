import json

from django.contrib import messages
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from suds import client
from cart.models import *
from order.forms import CouponForm
from .models import *


def OrderDetail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {'order': order, 'form': form}
    return render(request, 'order/order.html', context)


def OrderCreate(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(user_id=request.user.id, email=data['email'], f_name=data['f_name']
                                         , l_name=data['l_name'], address=data['address'])
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id
                                         , variant_id=c.variant_id, quantity=c.quantity)

            return redirect('order:order_detail', order.id)


@require_POST
def coupon_order(request, order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'the code expire or wrong', messages.error)
            return redirect('order:order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        messages.success(request, 'the discount was applied', )
    return redirect('order:order_detail', order_id)


"""
payment section    use zarin pal
"""
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09927641542'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify/'


def send_request(request, price, order_id):
    global amount
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request, price, order_id):
    global amount
    amount = price
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        # add custom things like paid true ...
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        cart = ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            if c.product.option_status == 'None':
                product = Products.objects.get(c.product.id)
                product.quantity -= c.quantity
                product.save()
            else:
                variant = variants.objects.get(c.variant.id)
                variant.amount -= c.quantity
                variant.save()
    # end custom section
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
