from django.db import models


class MobileManager(models.Manager):

    def __init__(self):
        self.queryset = super().get_queryset()

    def __sort(self, sort, ):
        if sort == 'newest':
            self.queryset = self.queryset.order_by('-published')
        if sort == 'oldest':
            self.queryset = self.queryset.order_by('published')

    def __filter_by_category(self, category):
        if category == 'mobile':
            self.queryset = self.queryset.filter(category='mobile')
        elif category == 'tablet':
            self.queryset = self.queryset.filter(category='tablet')
        else:
            pass
