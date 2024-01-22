import logging
import csv

from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from celery_app import celery_app
from apps.account.models import RegTry
from apps.product.bl import save_file_to_storage

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

    send_email_task.delay(**mail_data)
    print(f'Success {context["link"]}')

    logger.info(f'Send email to {mail_data["recipient_list"]}')
    try:
        mail.send_mail(**mail_data)
    except Exception as e:  # pylint: disable=broad-exception-caught
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
    reg_try.user = user
    reg_try.save()


@celery_app.task
def parsing_file(file_path):
    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                save_file_to_storage(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except csv.Error as e:
        print(f"CSV parsing error in file {file_path}: {e}")
