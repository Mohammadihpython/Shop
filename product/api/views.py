import rest_framework_simplejwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status, mixins

from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView

from product.models import Products, variants, Size, Color
from .serializer import ProductListSerializer, ProductDetailSerializer, VariantDetailSerializer
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS

from .paginations import ProductListPagination
from rest_framework import filters
import redis

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


class PostUserPermission(BasePermission):
    message = "editing only for owner user or admin"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.name == request.user


class ProductFilter(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['@name', ]

    # '^" starts-with search
    # '=' Exact matches
    # '@' Full_text search
    # '$' regex search
    def get_queryset(self):
        if 'product' in cache:
            products = cache.get('products', )
            return products
        else:
            products = Products.objects.all()
            return products


class ProductList(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductListSerializer
    permission_class = [DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = ProductListPagination

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    if Products.option_status == 'None':
        queryset = Products.objects.all()
        serializer_class = ProductDetailSerializer
    else:
        queryset = variants.objects.all()
        serializer_class = VariantDetailSerializer


class ProductDetailApi(APIView, PostUserPermission):
    lookup_field = 'id'
    print(lookup_field)
    lookup_url_kwarg = 'id'

    queryset = Products.objects.all()

    def get(self, request, id, *args, **kwargs):
        product = Products.objects.get(id=id)
        print(product)
        if product.option_status == 'None':
            print(True)
            try:
                queryset = Products.objects.filter(id=id)
                serializer = ProductDetailSerializer(instance=queryset, many=True).data
                return Response({'product': serializer, })
            except Products.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            print(False)
            try:
                queryset = variants.objects.filter(product_variant_id=id)
                serializer = VariantDetailSerializer(instance=queryset, many=True).data
                return Response({'product': serializer, })
            except variants.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class ProductUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    queryset = Products.objects.all()
    serializer_class = ProductDetailSerializer


class VariantUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = variants.objects.all()
    serializer_class = VariantDetailSerializer

