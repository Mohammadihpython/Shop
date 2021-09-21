from rest_framework import serializers
from product.models import Products, variants, Color, Size
from django.contrib.contenttypes import models
from drf_writable_nested import WritableNestedModelSerializer


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
            , 'amount', 'total_price',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    favourites = serializers.CharField(source='favourite_username', read_only=True)
    # product_variant = VariantDetailSerializer(many=True,)
    product_variant = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available', 'color', 'size',
            'description'
            , 'discount', 'total_price', 'option_status', 'likes', 'favourites', 'product_variant',)

    def get_product_variant(self, obj):
        queryset = variants.objects.filter(product_variant_id=obj.id)

        return VariantDetailSerializer(instance=queryset, many=True).data

    def get_color(self, obj):
        return ColorSerializer(instance=obj.color.all(), many=True).data

    def get_size(self, obj):
        return SizeSerializer(instance=obj.size.all(), many=True).data

    def create(self, validated_data):
        name = validated_data.get('name')
        quantity = validated_data.get('quantity')
        image = validated_data.get('image')
        price = validated_data.get('price')
        color = validated_data.get('color')
        size = validated_data.get('size')
        description = validated_data.get('description')
        discount = validated_data.get('discount')
        option_status = validated_data.get('option_status')

        product = Products(**validated_data)
        Products.objects.create(**validated_data)
        # product.save()
        for variant in validated_data['product_variant']:
            variant['product_variant_id'] = product.id
            new_variant = VariantDetailSerializer(data=variant)
            if new_variant.is_valid:
                variants.objects.create(**validated_data)
                # new_variant.save()
            else:
                product.delete()
                raise serializers.ValidationError(
                    {"variants": new_variant.errors})
        return product





class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'id', 'category', 'name', 'quantity', 'image', 'price', 'published', 'available',
            'description'
            , 'discount', 'total_price', 'option_status',)
