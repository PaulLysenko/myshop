import uuid
from django.db import models
from django.contrib.auth.models import User

from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings


class RegTry(models.Model):

    email = models.EmailField(unique=True, db_index=True)
    otc = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    c_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.email} at {self.c_time.strftime('%d-%m-%Y %H:%M:%S')}"

    def forming_mail(self, context):

        mail_data = {
            'subject': 'Please verify your account',
            'message': 'Please verify your account',
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [self.email],
            'html_message': render_to_string('registration_confirm.html', context=context),
        }
        return mail_data
        # todo: into function <--

    @staticmethod
    def send_reg_mail(mail_data, context):
        try:
            mail.send_mail(**mail_data)  # into celery task
            return print(f'success {context["link"]}')
        except Exception as exception:  # pylint: disable=W0703
            return f'[SENDMAIL] EXCEPTION {exception}'

    def user_creation(self, form):
        user = User.objects.create_user(
            username=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            email=self.email,
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )
        self.user = user
        self.save()
