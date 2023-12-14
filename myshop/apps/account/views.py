from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from apps.account.models import RegTry
from apps.account.forms import RegTryForm, ValidateRegTryForm


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

            if User.objects.filter(email=email_value).exists() or RegTry.objects.filter(email=email_value).exists():
                return HttpResponseBadRequest('Email is not valid.')

            reg_try = RegTry.objects.create(email=email_value)

            return redirect(reverse('validate_registration_try', kwargs={'otc': reg_try.otc}))
        return render(request, self.template_name, {'form': form})


class ValidateRegTryView(View):
    template_name = 'validate_regtry.html'

    def get(self, request, otc, *args, **kwargs):
        form = ValidateRegTryForm()

        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, otc):
        pass
