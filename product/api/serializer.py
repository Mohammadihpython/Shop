from rest_framework import serializers
from product.models import Products, variants, Color, Size
from django.contrib.contenttypes import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name',)


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('name',)


class VariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = variants
        fields = (
            'id', 'name', 'product_variant', 'color_variant', 'size_variant', 'unit_price', 'discount'
            , 'amount', 'total_price'
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    favourites = serializers.CharField(source='favourite_username', read_only=True)

    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available', 'color', 'size',
            'description'
            , 'discount', 'total_price', 'option_status', 'likes', 'favourites', )

    def get_color(self, obj):
        return ColorSerializer(instance=obj.color.all(), many=True).data

    def get_size(self, obj):
        return SizeSerializer(instance=obj.size.all(), many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available',
            'description'
            , 'discount', 'total_price', 'option_status',)
