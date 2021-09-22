from rest_framework import serializers
from order.models import ItemOrder, Order, Coupon


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user',
            'paid',
            'create',
            'email',
            'f_name',
            'l_name',
            'address'
        )


class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = (
            'order',
            'user',
            'quantity',
            'product',
            'variant',
        )


class CouponCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
