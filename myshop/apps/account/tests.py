from django.test import TestCase
from django.urls import reverse
from uuid import uuid4


class RegistrationTests(TestCase):
    def test_registration_url(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_registration_confirm_url(self):
        otc_value = str(uuid4())
        response = self.client.get(reverse('registration_confirm', args=[otc_value]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_confirm.html')


