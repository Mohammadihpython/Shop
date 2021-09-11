from rest_framework import generics
from product.models import Products, variants, Size, Color
from .serializer import ProductSerializer
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS


class PostUserPermission(BasePermission):
    message = "editing only for owner user or admin"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.name == request.user


class Product_list(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_class = [DjangoModelPermissionsOrAnonReadOnly]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView, PostUserPermission):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
