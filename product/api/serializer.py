from rest_framework import serializers
from product.models import Products, variants


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available', 'color', 'size',
            'description'
            , 'discount', 'total_price', 'option_status',)


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = variants
        fields= (
            'id','name', 'product_variant', 'color_variant', 'size_variant', 'unit_price', 'discount'
            ,'amount', 'total_price'
        )