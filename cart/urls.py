from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView, name='cart_detail'),
    path('add/<int:id>/', views.Add_Cart, name='add_cart'),
    path('del/<int:id>/', views.Del_Cart, name='del_cart'),
]
