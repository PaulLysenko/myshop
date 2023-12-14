from uuid import uuid4
from unittest import skip

from django.test import TransactionTestCase, Client
from django.urls import reverse
from apps.account.models import RegTry


class SmokeTestRegTry(TransactionTestCase):

    def setUp(self):
        self.client = Client()

    def test_get_regtry(self):
        url = reverse('registration_try')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    # @skip('FIXME')
    def test_successful_registration_try(self):
        url = reverse('registration_try')
        data = {'email': 'qwerty@test.com'}
        result = self.client.post(url, data=data)
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(result, reverse('validate_registration_try',
                                             kwargs={'otc': RegTry.objects.last().otc}))

    def test_duplicate_email_registration(self):
        RegTry.objects.create(email='qwerty@test.com', otc=uuid4())
        data = {'email': 'qwerty@test.com'}
        result = self.client.post(reverse('registration_try'), data=data)
        self.assertEqual(result.status_code, 400)
        self.assertContains(result, 'Email is not valid.')

    def tearDown(self):
        RegTry.objects.all().delete()
