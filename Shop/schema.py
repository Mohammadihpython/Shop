import graphene
from graph.product.queries import ProductQuery


class Query(ProductQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
