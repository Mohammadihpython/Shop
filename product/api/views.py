from rest_framework import generics
from product.models import Products, variants, Size, Color
from .serializer import ProductSerializer


class Product_list(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
