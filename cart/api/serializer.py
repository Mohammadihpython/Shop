from rest_framework import serializers
from product.api.serializer import ProductDetailSerializer
from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = Cart
        fields = (
            'user',
            'product',
            'variant',
            'quantity',
        )


class CartDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'user',
            'product',
            'variant',
            'quantity',
        )
