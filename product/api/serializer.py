from rest_framework import serializers
from product.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available', 'color', 'size',
            'description'
            , 'discount', 'total_price', 'option_status',)
