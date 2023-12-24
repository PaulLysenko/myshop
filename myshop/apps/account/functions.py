from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User


def send_registration_email(reg_try):
    link = f'http://{settings.HOST_NAME}/registration/{reg_try.otc}'

    context = {
        'link': link,
        # more data here for customization of the email?
    }

    mail_data = {
        'subject': 'Please verify your account',
        'message': 'Please verify your account',
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': [reg_try.email],
        'html_message': render_to_string('registration_confirm.html', context=context),
    }

    try:
        send_mail(**mail_data)  # into Celery task
        print(f'success {link}')
    except Exception as exception:  # pylint: disable=W0703
        print(f'[SENDMAIL] EXCEPTION {exception}')


def create_user_and_link(reg_try, form):
    user = User.objects.create_user(
        username=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
        email=reg_try.email,
        password=form.cleaned_data['password'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
    )
    reg_try.user = user
    reg_try.save()