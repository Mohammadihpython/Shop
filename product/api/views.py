from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from product.models import Products, variants, Size, Color
from .serializer import ProductSerializer
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS, \
    DjangoModelPermissions
from rest_framework import viewsets


class PostUserPermission(BasePermission):
    message = "editing only for owner user or admin"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.name == request.user


#
# class Product_list(generics.ListCreateAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     permission_class = [DjangoModelPermissionsOrAnonReadOnly]
#
#
# class ProductDetail(generics.RetrieveUpdateDestroyAPIView, PostUserPermission):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer

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

class ProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_class = [DjangoModelPermissions]
    # override methods

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Products, slug=item)
        
    def get_queryset(self):
        return Products.objects.all()
    