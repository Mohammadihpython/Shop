import graphene
from .types import ProductType, VariantType
from product.models import Products, variants
from django.core.cache import cache


class ProductQuery(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, pk=graphene.ID())

    product_variants = graphene.List(VariantType, pk=graphene.ID())

    def resolve_products(root, info):
        # query a list of product
        return Products.objects.all()

    def resolve_product(root, info, pk):
        # query a list of product
        product = Products.objects.get(id=pk)

        return product

    def resolve_product_variants(root, info, pk):
        return variants.objects.filter(product_variant_id=pk)
