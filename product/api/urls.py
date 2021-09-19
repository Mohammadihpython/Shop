from django.urls import path

from .views import *
# from .views import ProductView
# from rest_framework.routers import DefaultRouter


app_name = 'apiItem'
urlpatterns = [
    path('', ProductList.as_view(), name='api_list_create'),
    path('search/', ProductFilter.as_view(), name='api_list_search'),
    path('<int:id>/', ProductDetailApi.as_view(), name='product_Detail'),
    path('favourita/<int:id>/', FavouriteAddDell.as_view(), name='favourite_add'),
    path('like/<int:id>/', LikeAddDell.as_view(), name='like_add'),
    path('update/<int:id>/', ProductUpdateDestroyApi.as_view(), name='product_update'),
    path('varupdate/<int:id>/', VariantUpdateDestroyApi.as_view(), name='variant_update'),

]
# app_name = 'apiItem'
# router = DefaultRouter()
# router.register('', ProductView,basename='product')
# urlpatterns = router.urls
