from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from apps.account.forms import RegistrationForm, AcceptRegistrationForm
from apps.account.models import RegTry


# from apps.account.forms import RegTryForm, ValidateRegTryForm

class RegistrationView(View):
    template_name = 'regtry.html'

    def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form,
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email_value = form.cleaned_data['email']

            if User.objects.filter(email=email_value).exists():
                return HttpResponse('Email is not valid.')
            if RegTry.objects.filter(email=email_value).exists():
                return HttpResponse('This email is already tried to register.')

            reg_try = RegTry.objects.create(email=email_value)

            return redirect(reverse('registration_confirm', kwargs={'otc': reg_try.otc}))
        return render(request, self.template_name, {'form': form})


class RegistrationConfirmView(View):
    template_name = 'reg_accept.html'

    def get(self, request, otc, *args, **kwargs):
        form = AcceptRegistrationForm

        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)
