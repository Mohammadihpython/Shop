
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from graphene_django.views import GraphQLView

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Shop.schema import schema

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('account/', include('account.urls', namespace='account')),

    path('cart/', include('cart.urls', namespace='cart', )),
    path('api/cart/', include('cart.api.urls', namespace='apiCart', )),

    path('', include('product.urls', namespace='product', )),

    path('comment/', include('comment.urls', namespace='comment', )),
    path('api/comment/', include('comment.api.urls', namespace='apiComment', )),

    path('search/', include('search.urls', namespace='search', )),

    path('order/', include('order.urls', namespace='order', )),
    path('api/order/', include('order.api.urls', namespace='apiOrder', )),

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
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
)
