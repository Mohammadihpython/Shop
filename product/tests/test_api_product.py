from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from product.models import *
from django.contrib.auth import get_user_model
from django.urls import reverse as api_reverse

user = get_user_model()


class ProductTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.testuser1 = user.objects.create_superuser(
            username='ali', password='1234', email='ali@yahoo.com'
        )
        Color.objects.create(name="red")
        variants.objects.create(name='A30', color_variant_id='1', unit_price='410000', amount='40',
                                product_variant_id=1)
        Products.objects.create(name='A30', quantity=4, image='A30',
                                slug="A30", price=4000, option_status="color")

    def test_favourite_add(self):
        url = api_reverse('apiItem:favourite_add', kwargs={'id': '1'})
        self.client.login(username=self.testuser1.username,
                          password='1234')

        response = self.client.post(url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_add(self):
        url = api_reverse('apiItem:like_add', kwargs={'id': '1'})
        self.client.login(username=self.testuser1.username,
                          password='1234')

        response = self.client.post(url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_product(self):
        url = api_reverse('apiItem:api_list_create', )
        response = self.client.get(url, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        # self.client.login(username=self.testuser1.username,
        #              password=1234, email='ali@yahoo.com')
        self.client.login(username=self.testuser1.username,
                          password='1234')

        data = {'name': 'A20', 'quantity': '5',
                'price': '2000',
                'slug': 'A20'}
        url = api_reverse('apiItem:api_list_create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update(self):
        client = APIClient()

        client.login(username=self.testuser1.username,
                     password=1234, email='ali@yahoo.com')

        url = reverse('apiItem:product_update', kwargs={'id': 1})
        urlvar = reverse('apiItem:variant_update', kwargs={'id': 1})
        response = client.put(
            url, {
                'name': 'A30',
                'quantity': 4,
                'slug': "A30",
                'price': 4000,
                'discount': '50',
                'option_status': "color"
            }, format='json')
        responsevar = client.put(
            urlvar, {
                "id": 1,
                "name": "A80",
                "product_variant": {
                    "id": 1,
                    "favourites": "",
                    "likes": "",
                    "like_count": -1
                },
                "color_variant": 1,
                "size_variant": "",
                "unit_price": 4100000,
                "discount": 20,
                "amount": 50,
                "total_price": 3280000
            },format='json'

        )
        print(response.data)
        print(responsevar.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(responsevar.status_code, status.HTTP_200_OK)
