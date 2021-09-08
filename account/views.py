from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth.views import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from pytz import utc

from product.models import Products
from .models import UserOTP
from .tasks import send_remember_password_code

from account.forms import CustomRegister, LoginWithEmail, RememberEmailPasswordForm, \
    VerifyRememberEmailPasswordSMS

User = get_user_model()


@login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Products, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })


# Create your views here.
class RegisterView(FormView):
    model = User
    form_class = CustomRegister
    template_name = 'account/register.html'
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        form.save()
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product:product_list')


class LoginView(FormView):
    form_class = LoginWithEmail
    template_name = 'account/login.html'
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product:product_list')


# class LoginWithEmailView(FormView):
# form_class = LoginWithEmail
# template_name = 'account/Login.html'
# success_url = 'mobile/shop.html'

# $def form_valid(self, form):
#  login(self.request, form.cleaned_data['user'])
# return super().form_valid(form)


class RememberEmailPasswordView(FormView):
    form_class = RememberEmailPasswordForm
    template_name = 'account/RememberEmail.html'
    success_url = reverse_lazy('product/product_list')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        code = get_random_string(length=6, allowed_chars="0123456789abcdef")
        print(code)
        send_remember_password_code.delay(email, code)
        self.request.session['email'] = email
        OTP_code = UserOTP.objects.create(
            code=code, code_type=UserOTP.EMAIL,
            expire_time_end=(datetime.now().replace(tzinfo=utc) + timedelta(
                minutes=1)),
            email=email
        )
        return HttpResponseRedirect(reverse_lazy("account:VerifyCode"))


class VerifyEmailCodeView(FormView):
    form_class = VerifyRememberEmailPasswordSMS
    template_name = 'account/VerifyEmailCode.html'
    success_url = reverse_lazy('product/product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        form.sign_in()
        del self.request.session["email"]
        return super().form_valid(form)


def LogOutView(request):
    logout(request)
    return redirect('product:product_list')
