import uuid

from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.account.forms import RegTryForm, ValidateRegTryForm
from apps.account.models import RegTry


class RegTryView(View):
    template_name = 'registration_try.html'
    template_name2 = 'validate_regtry.html'

    def get(self, request):
        form = RegTryForm()
        context = {
            'form': form,
        }

        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):
        form = RegTryForm(request.POST)

        if form.is_valid():
            email_value = form.cleaned_data['email']
            otc_value = uuid.uuid4()

            try:
                reg_try = RegTry.objects.create(email=email_value, otc=otc_value)
            except:
                if User.objects.filter(email=email_value).exists() or RegTry.objects.filter(email=email_value).exists():
                    raise HttpResponseBadRequest('Email is not valid.')

            return redirect(reverse('validate_registration_try', kwargs={'otc': reg_try.otc}))


class ValidateRegTryView(View):
    template_name = 'validate_regtry.html'

    def get(self, request, otc, *args, **kwargs):
        form = ValidateRegTryForm()

        try:
            reg_try = RegTry.objects.get(otc=otc, user_id__isnull=True)
        except:
            raise HttpResponseBadRequest('Invalid.')

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, otc):
        pass
