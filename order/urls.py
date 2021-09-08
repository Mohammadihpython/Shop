from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('create/', views.OrderCreate, name='order_create'),
    path('<int:order_id>/', views.OrderDetail, name='order_detail'),
    path('coupon/<int:order_id>/', views.coupon_order, name='coupon'),
    path('request/<int:price>/<int:order_id>/', views.send_request, name='request'),
    path('verify/<int:price>/<int:order_id>/', views.verify, name='verify'),
]

