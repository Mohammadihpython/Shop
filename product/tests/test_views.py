from unittest import skip

from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import *
from product.views import ProductView


@skip("skip test")
class testSkip(TestCase):
    def test_skip(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        self.color = Color.objects.create(name="red")
        self.size = Size.objects.create(name='xl')
        Products.objects.create(image='A20', name="A20", quantity=5,
                                price='2000',
                                slug='A20')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='')
        self.assertEqual(response.status_code, 400)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(
            reverse('product:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(
            reverse('product:product-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        response = ProductView(request)
        html = response.content.decode('utf8')
        # self.assertIn('<dive>', html)
        # self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Example: Using request factory
        """
        request = self.factory.get('/')
        response = ProductView(request)
        html = response.content.decode('utf8')
        # self.assertIn('<div>', html)
        # self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
