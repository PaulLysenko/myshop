from django.test import TestCase, Client
from django.urls import reverse


class SmokeTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def setUp(self):
        pass

    def test_get_products(self):
        url = reverse('products')
        print(f'--url >> {url}')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

        def test_post_products(self):
            url = reverse('products')
            print(f'--url >> {url}')
            result = self.client.post(url, data={'search': 'abcd'})
            self.assertEqual(result.status_code, 200)

        def test_get_product_no_product(self):
            url = reverse('product', args=(1,))
            print(f'--url >> {url}')
            result = self.client.post(url, data={'search': 'abcd'})
            self.assertEqual(result.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass
