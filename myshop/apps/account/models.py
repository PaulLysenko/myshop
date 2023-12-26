import uuid

from django.conf import settings
from django.core import mail
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class RegTry(models.Model):

    email = models.EmailField(unique=True, db_index=True)
    otc = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    c_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def send_reg_mail(self):
        context = {
            'link': f'http://{settings.HOST_NAME}/registration/{self.otc}',
            # more data here for customisation email?
        }
        mail_data = {
            'subject': 'Please verify your account',
            'message': 'Please verify your account',
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [self.email],
            'html_message': render_to_string('registration_confirm.html', context=context),
        }

        try:
            mail.send_mail(**mail_data)  # into celery task
            print(f'success {context["link"]}')
        except Exception as exception:  # pylint: disable=W0703
            print(f'[SENDMAIL] EXCEPTION {exception}')

    def __str__(self):
        return f"{self.email} at {self.c_time.strftime('%d-%m-%Y %H:%M:%S')}"
