import rest_framework_simplejwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView

from product.models import Products, variants, Size, Color
from .serializer import ProductListSerializer, ProductDetailSerializer, VariantDetailSerializer
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS, \
    DjangoModelPermissions
from rest_framework import viewsets
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


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    if Products.option_status == 'None':
        queryset = Products.objects.all()
        serializer_class = ProductDetailSerializer
    else:
        queryset = variants.objects.all()
        serializer_class = VariantDetailSerializer


class ProductDetailApi(GenericAPIView):
    lookup_field = id
    lookup_url_kwarg = id
    queryset = Products.objects.all()

    def get(self, request, id):
        if Products.option_status == 'None':
            try:
                queryset = Products.objects.filter(id=id)
                serializer = ProductDetailSerializer(instance=queryset, many=True).data
                return Response({'product': serializer, })
            except Products.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            try:
                queryset = variants.objects.filter(product_variant_id=id)
                serializer = VariantDetailSerializer(instance=queryset, many=True).data
                return Response({'product': serializer, })
            except variants.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    # def get_serializer_class(self):
    #     if Products.option_status == 'None':
    #         serializer = ProductDetailSerializer(instance=self.queryset, many=True).data
    #         return Response({'product': serializer, })
    #     else:
    #         try:
    #             serializer = VariantDetailSerializer(instance=self.queryset, many=True).data
    #             return Response({'product': serializer, })
    #         except variants.DoesNotExist:
    #             return Response(status=status.HTTP_404_NOT_FOUND)

# work with viewsts and ruter
# class ProductView(viewsets.ViewSet):
#     queryset = Products.objects.all()
#     permission_class = [DjangoModelPermissionsOrAnonReadOnly]
#
#     def list(self,request):
#         serializer_class = ProductSerializer(self.queryset,many=True)
#         return Response(serializer_class.data)
#
#     def retrieve(self,request,pk=None):
#         product =get_object_or_404(self.queryset, pk =pk)
#         serializer_class = ProductSerializer(product)
#         return Response(serializer_class.data)

# class ProductView(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     permission_class = [DjangoModelPermissions]
#
#     # override methods
#
#     def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404(Products, slug=item)
#
#     def get_queryset(self):
#         return Products.objects.all()
