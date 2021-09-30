from django.contrib.auth import get_user_model
from graphene import relay

from product.models import Products, variants, Color, Size
import graphene
from graphene_django import DjangoObjectType

user = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = user
        fields = ('username', 'like', 'favourite')


class ProductType(DjangoObjectType):
    total_price = graphene.String(source='total_price')

    class Meta:
        model = Products
        fields = ('name', 'likes', 'favourites',
                  'category', 'slug', 'published', 'modified_time',
                  'color',
                  'size',
                  'description',
                  'discount',
                  'option_status',
                  'like_count',
                  "image", 'price',)
        interfaces = (relay.Node,)
        total_price = graphene.String()

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
            return self.image


class VariantType(DjangoObjectType):
    class Meta:
        model = variants
        fields = '__all__'
        interfaces = (relay.Node,)


#
class ColorType(DjangoObjectType):
    class Meta:
        model = Color
        fields = '__all__'


class SizeType(DjangoObjectType):
    class Meta:
        model = Size
        fields = '__all__'
