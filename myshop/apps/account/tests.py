from django.test import TransactionTestCase, Client
from django.urls import reverse
from apps.account.models import RegTry


class SmokeTestRegTry(TransactionTestCase):

    def setUp(self):
        self.client = Client()

    def test_get_regtry(self):
        url = reverse('registration try')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_post_regtry(self):
        url = reverse('registration try')
        result = self.client.post(url, data={'email': 'test@qwerty.com'})
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(result, reverse('validate registration try',
                                             kwargs={'otc': RegTry.objects.first().otc}))

    def test_post_regtry_duplicate_email(self):
        RegTry.objects.create(email='test@qwerty.com', otc='test_otc')
        result = self.client.post(reverse('registration try'), data={'email': 'test@qwerty.com'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration_try.html')
        self.assertContains(result, 'Email is already registered.')

    def test_post_regtry_duplicate_regtry(self):
        RegTry.objects.create(email='test@qwerty.com', otc='test_otc')
        result = self.client.post(reverse('registration try'), data={'email': 'test@qwerty.com'})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'registration_try.html')
        self.assertContains(result, 'You\'ve already attempted to register that email.')
