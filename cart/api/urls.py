from django.urls import path

from .views import CartDelApiView, CartListApiView, ADDCartApiView

app_name = 'apiCart'
urlpatterns = [
    # user Apis
    path('', CartListApiView.as_view(), name='api_list'),
    path('delcart/', CartDelApiView.as_view(), name='api_del_cart'),
    path('addcart/', ADDCartApiView.as_view(), name='api_add_cart'),
]
