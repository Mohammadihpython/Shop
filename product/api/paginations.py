from rest_framework.pagination import LimitOffsetPagination


class ProductListPagination(LimitOffsetPagination):
    max_limit = 10
    default_limit= 6