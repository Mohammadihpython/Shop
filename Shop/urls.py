"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('account/', include('account.urls', namespace='account')),
    path('cart/', include('cart.urls', namespace='cart', )),
    path('api/cart/', include('cart.api.urls', namespace='apiCart', )),
    path('', include('product.urls', namespace='product', )),
    path('comment/', include('comment.urls', namespace='comment', )),
    path('search/', include('search.urls', namespace='search', )),
    path('order/', include('order.urls', namespace='order', )),
    path('api/account/', include('account.api.urls', namespace='apiAccount', )),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/item/', include('product.api.urls', namespace='apiItem', )),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework', )),
    path('docs/', include_docs_urls(title="HamedShop")),
    path('openapi', get_schema_view(
        title="HamedShop",
        description="api for shop and product",
        version="1.0.0",
    ), name='openapi-schema'
         ),

]
