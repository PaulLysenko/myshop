import logging
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from celery_app import celery_app

from apps.account.models import RegTry, Profile

logger = logging.getLogger(__name__)


@celery_app.task
def send_email_task(otc, email):

    context = {
        'link': f'http://{settings.HOST_NAME}/registration/{otc}',

    }
    mail_data = {
        'subject': 'Please verify your account',
        'message': 'Please verify your account',
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': [email],
        'html_message': render_to_string('registration_confirm.html', context=context),
    }

    logger.info(f'Success {context["link"]}')

    logger.info(f'Send email to {mail_data["recipient_list"]}')
    try:
        mail.send_mail(**mail_data)
    except Exception as e:
        logger.error(f'Error email sending: {e}')


@celery_app.task
def process_registration_task(data, reg_try_id):
    reg_try = RegTry.objects.get(id=reg_try_id)
    user = User.objects.create_user(
        username=f"{data['first_name']} {data['last_name']}",
        email=reg_try.email,
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
    )
    Profile.objects.create(user=user)
    reg_try.user = user
    reg_try.save()
