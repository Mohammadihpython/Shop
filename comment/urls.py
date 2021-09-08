from django.urls import path
from . import views
from .views import Product_comment

app_name = 'comment'
urlpatterns = [
    path('comment/<int:id>/', views.Product_comment, name='Product_comment'),
]
