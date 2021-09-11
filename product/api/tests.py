from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from product.models import *
from django.contrib.auth import get_user_model

user = get_user_model()


class ProductTest(APITestCase):

    def test_view_product(self):
        url = reverse('apiItem:api_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_product(self):
        data = {'image': 'A20', 'name': "A20", 'quantity': '5',
                'price': '2000',
                'slug': 'A20'}
        url = reverse('apiItem:product_Detail')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        root = reverse('apiItem:product_Detail', kwargs={'pk': 1})
        response = self.client.get(root, format='json')

    def test_post_update(self):
        client = APIClient()
        self.testuser1 = user.objects.create_superuser(
            username='ali', password='1234', email='ali@yahoo.com'
        )
        Color.objects.create(name="red")
        variants.objects.create(name='A30', color_variant_id='1', unit_price='410000', amount='40',
                                product_variant_id=1)
        Products.objects.create(name='A30', quantity=4, image='A30',
                                slug="A30", price=4000, option_status="color")

        client.login(username=self.testuser1.username,
                     password=1234, email='ali@yahoo.com')

        url = reverse('apiItem:product_Detail', kwargs={'pk': 1})
        response = client.put(
            url, {
                'name': 'A30',
                'quantity': 4,
                'slug': "A30",
                'price': 4000,
                'discount':'50',
                'option_status': "color"
            },format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
