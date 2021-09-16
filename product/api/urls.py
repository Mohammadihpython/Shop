from django.urls import path

from .views import ProductList,ProductDetailApi,ProductFilter
# from .views import ProductView
# from rest_framework.routers import DefaultRouter


app_name = 'apiItem'
urlpatterns = [
    path('', ProductList.as_view(), name='api_list_create'),
    path('search/', ProductFilter.as_view(), name='api_list_search'),
    path('<int:id>/', ProductDetailApi.as_view(), name='product_Detail'),

]
# app_name = 'apiItem'
# router = DefaultRouter()
# router.register('', ProductView,basename='product')
# urlpatterns = router.urls
