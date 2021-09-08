from django.urls import path

from . import views
from .views import RegisterView, LoginView,  RememberEmailPasswordView,VerifyEmailCodeView
app_name = "account"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView, name='logout'),
    path('like/', views.like, name='like'),
    path('RememberPassword/', RememberEmailPasswordView.as_view(), name='forgot_pass'),
    path('VerifyPassword/', VerifyEmailCodeView.as_view(), name='VerifyCode'),
]
