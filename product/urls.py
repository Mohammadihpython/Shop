from django import views
from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path('', views.ProductView, name='product_list'),
    path('<str:pk>/', views.ProductDetailView, name='product-detail'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
]
