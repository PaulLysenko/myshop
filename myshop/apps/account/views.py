from gettext import gettext as _

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from apps.account.models import RegTry
from apps.account.forms import RegTryForm, ValidateRegTryForm
from apps.account.utilities import user_creation


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
        reg_try.send_reg_mail()

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

        user_creation(form, reg_try)
        return redirect(reverse('home'))
