from gettext import gettext as _

from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from apps.account.models import RegTry
from apps.account.forms import RegTryForm, ValidateRegTryForm


class RegTryView(View):
    template_name = 'registration_try.html'

    def get(self, request):
        form = RegTryForm()
        context = {
            'form': form,
        }

        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):
        form = RegTryForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        email_value = form.cleaned_data['email']

        if User.objects.filter(email=email_value).exists() or RegTry.objects.filter(email=email_value).exists():
            return render(request, 'invalid_data.html', {'data': 'Email is not valid.'}, status=400)

        reg_try = RegTry.objects.create(email=email_value)

        # todo: into function send_reg_mail->
            # todo: into function -->
        context = {
            'link': f'http://{settings.HOST_NAME}/registration/{reg_try.otc}',
            # more data here for customisation email?
        }
        mail_data = {
            'subject': 'Please verify your account',
            'message': 'Please verify your account',
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [reg_try.email],
            'html_message': render_to_string('registration_confirm.html', context=context),
        }
            # todo: into function <--

        try:
            mail.send_mail(**mail_data)  # into celery task
            print(f'success {context["link"]}')
        except Exception as exception:  # pylint: disable=W0703
            print(f'[SENDMAIL] EXCEPTION {exception}')

        # todo: into function send_reg_mail <-

        return redirect(reverse('home'))


class ValidateRegTryView(View):
    template_name = 'validate_regtry.html'

    def get(self, request, otc):
        form = ValidateRegTryForm()

        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, otc):
        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        form = ValidateRegTryForm(request.POST)

        if not form.is_valid():

            context = {
                'otc': reg_try.otc,
                'form': form,
            }

            return render(request, self.template_name, context=context)

        # todo:  into function ->
        user = User.objects.create_user(
            username=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            email=reg_try.email,
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )
        reg_try.user = user
        reg_try.save()
        # todo:  into function <-

        return redirect(reverse('home'))
