from datetime import datetime, timedelta, time

from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from pytz import utc

from account.models import UserOTP

User = get_user_model()


class CustomRegister(forms.Form):
    email = forms.EmailField(label=_('email'))
    username = forms.CharField(max_length=150, label=_('username'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(_("username already exists"))

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_("email already exists"))
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        # send_confirm_email(user)
        # send_confirm_code(user)
        # send_phone_verification_code.delay(user.username)
        #  send_phone_verification_code.apply_async([user.username])
        self.cleaned_data['user']=user
        return self.cleaned_data


class loginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        if "email" not in self.cleaned_data:
            raise forms.ValidationError(_("Username Field is Required :)"))
        if "password" not in self.cleaned_data:
            raise forms.ValidationError(_("Password Field is Required"))
        user = User.objects.filter(
            email=self.cleaned_data["email"]).first()
        if user is None:
            raise forms.ValidationError(
                _("User with provided username does not exists"))
        if not user.check_password(self.cleaned_data["password"]):
            raise forms.ValidationError(_("Wrong password"))
        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(
                _("Unable login with provided credentials"))
        self.cleaned_data['user'] = user
        return self.cleaned_data


class LoginWithEmail(forms.Form):
    email = forms.EmailField(required=True, help_text="please enter your Email")
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        if "email" not in self.cleaned_data:
            raise forms.ValidationError(_('please enter your Email'))
        user = User.objects.filter(email=self.cleaned_data['email']).first()
        if user is None:
            raise forms.ValidationError(_('user is not exist'))
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(_('wrong password'))
        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(
                _("Unable login with provided credentials"))
        self.cleaned_data['user'] = user

        return self.cleaned_data


class RememberEmailPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        user = User.objects.filter(email=self.cleaned_data['email']).first()
        if user is None:
            raise forms.ValidationError(_('*****user is not exists ******'))
        return self.cleaned_data


class VerifyRememberEmailPasswordSMS(forms.Form):
    code = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        user_code = UserOTP.objects.filter(code_type=UserOTP.EMAIL,
                                           email=self.request.session[
                                               'email']).last()

        user_code_expire_time = user_code.time_in_range(
            user_code.expire_time_start, user_code.expire_time_end,
            datetime.now().replace(tzinfo=utc))

        if self.cleaned_data['code'] != user_code.code:
            raise forms.ValidationError(_("This code is not True"))
        if user_code_expire_time is False:
            raise forms.ValidationError(_('This code is expired'))
        return self.cleaned_data

    def sign_in(self):
        user = authenticate(
            self, request=self.request,
            email=self.request.session["email"]
        )
        login(self.request, user)
        return user
