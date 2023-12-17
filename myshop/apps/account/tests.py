from django.test import TestCase
from django.urls import reverse
from .models import RegTry


class RegistrationTests(TestCase):
    def test_registration_view_get(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_registration_view_post(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 302)

    def test_confirm_registration_view_get_valid_otc(self):
        regtry = RegTry.objects.create(email='test@example.com')
        response = self.client.get(reverse('confirm_registration', args=[regtry.otc]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')


