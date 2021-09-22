from django.urls import path
from .views import OrderCreateApiView, OrderListDestroyApiView, OrderDeleteApiView

app_name = 'apiOrder'
urlpatterns = [
    path('create/', OrderCreateApiView.as_view(), name='order_create'),
    path('', OrderListDestroyApiView.as_view(), name='order_list'),
    path('remove/<int:id>/', OrderDeleteApiView.as_view(), name='order_remove'),
]
