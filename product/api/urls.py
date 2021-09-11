from django.urls import path
from . import views
# from .views import Product_list,ProductDetail
from .views import ProductView
from rest_framework.routers import DefaultRouter


# app_name = 'apiItem'
# urlpatterns = [
#     path('', Product_list.as_view(), name='api_list_create'),
#     path('<int:pk>/', ProductDetail.as_view(), name='product_Detail'),
#
# ]
app_name = 'apiItem'
router = DefaultRouter()
router.register('', ProductView,basename='product')
urlpatterns = router.urls
