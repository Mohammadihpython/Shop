from unittest import skip
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import *


class Test_Product_Model(TestCase):
    @classmethod
    def setUp(cls):
        cls.c = Client()
        cls.factory = RequestFactory()
        Products.objects.create(name='A30', quantity=4, image='A30',
                                slug="A30", price=4000, option_status="color")
        Color.objects.create(name="red")

        variants.objects.create(name='A30', color_variant_id='1', unit_price='410000', amount='40', product_variant_id=1)

    def test_product_content(self):
        product = Products.objects.get(id=1)
        name = f'{product.name}'
        image = f'{product.image}'
        slug = f'{product.slug}'
        price = f'{product.price}'
        option_status = f'{product.option_status}'
        quantity = f'{product.quantity}'
        self.assertEqual(name, 'A30')
        self.assertEqual(image, 'A30')
        self.assertEqual(slug, 'A30')
        self.assertEqual(price, '4000')
        self.assertEqual(option_status, 'color')
        self.assertEqual(quantity, '4')
        self.assertEqual(str(product), 'A30')

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(
            reverse('product:product-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
