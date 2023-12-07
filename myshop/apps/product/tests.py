from django.test import TransactionTestCase, Client
from django.urls import reverse
from apps.product.models import Product


class SmokeTestProducts(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def setUp(self):
        pass

    def test_get_products(self):
        url = reverse('products')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_post_products(self):
        url = reverse('products')
        result = self.client.post(url, data={'search': 'abcd'})
        self.assertEqual(result.status_code, 200)


class SmokeTestProduct(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_get_product_existing_product(self):
        product = Product.objects.create(
            name='abcd',
            price=1,
        )
        url = reverse('product', args=(product.id, ))
        result = self.client.post(url, data={'search': 'abcd'})
        self.assertEqual(result.status_code, 200)

    def test_get_product_no_products(self):
        url = reverse('product', args=(1, ))
        result = self.client.post(url, data={'search': 'abcd'})
        self.assertEqual(result.status_code, 404)
