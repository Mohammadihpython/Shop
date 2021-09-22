from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from product.manager import MobileManager

User = get_user_model()


def upload_to(instance, filename):
    return 'product/{}'.format(filename)


class Color(models.Model):
    name = models.CharField(verbose_name=_('color'), blank=True, null=True, max_length=160)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(verbose_name=_('size'), blank=True, null=True, max_length=50)

    def __str__(self):
        return self.name


class Products(models.Model):
    TYPE_CHOICE = (
        ('MOBILE', "mobile"),
        ('TABLET', "tablet"),
        ('CLOTHES', "clothes"),
    )
    status = (

        ('None', 'None'),
        ('color', 'color'),
        ('size', 'size'),
    )

    category = models.CharField(_("code type"), choices=TYPE_CHOICE, blank=True, null=True, max_length=150)
    name = models.CharField(verbose_name=_("name"), max_length=250)
    quantity = models.PositiveIntegerField(default=0, verbose_name=_('quantity'))
    image = models.ImageField(upload_to=upload_to, verbose_name=_('image'), null=True, blank=True,
                              default='products/default.png')
    slug = models.SlugField(unique=True, null=True)
    price = models.PositiveIntegerField(verbose_name=_('(price'))
    published = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    available = models.BooleanField(verbose_name=_('available'), default=True)
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_('updated_time'))
    color = models.ManyToManyField(Color, blank=True, related_name='color', related_query_name='color')
    size = models.ManyToManyField(Size, blank=True, related_query_name='size')
    description = models.TextField(max_length=10000, verbose_name=_('description'), blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField(blank=True, null=True)
    option_status = models.CharField(max_length=150, default='None', blank=True, null=True, choices=status)
    likes = models.ManyToManyField(User, blank=True, related_name='like', default=None)
    like_count = models.BigIntegerField(default='0')

    favourites = models.ManyToManyField(User, blank=True, related_name='favourite', default=None)
    objects = MobileManager

    class meta:
        db_table = _('item')
        verbose_name = _('item')
        verbose_name_plural = _('item')

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id])

    def like_username(self):
        return "-".join(like.username for like in self.likes.all())

    def favourite_username(self):
        return '*'.join(favourite.username for favourite in self.favourites.all())

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if self.discount:
            total = (self.discount * self.price) / 100
            print(total)
            return int(self.price - total)

        elif not self.discount:
            return int(self.price)
        return self.total_price


class variants(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name'))
    product_variant = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size_variant = models.ForeignKey(Size, verbose_name=_("size"), on_delete=models.CASCADE, blank=True, null=True)
    unit_price = models.PositiveIntegerField(verbose_name=_('unit-price'))
    discount = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(default=1, verbose_name=_('amount'))
    total_price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        name = [str(self.name), str(self.color_variant), str(self.size_variant)]
        return '_'.join(name)

    @property
    def total_price(self):
        if self.discount:
            total = (self.discount * self.unit_price) / 100
            print(total)
            return int(self.unit_price - total)
        elif not self.discount:
            return int(self.unit_price)

        return self.total_price
