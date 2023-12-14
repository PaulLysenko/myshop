from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegistrationForm

from .forms import RegTryForm
from .models import RegTry


class RegTryView(View):
    template_name = 'RegTry.html'
    template_name2 = 'registration_confirm.html'

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
                return HttpResponse('Email is not valid.')

            reg_try = RegTry.objects.create(email=email_value)

            return redirect(reverse('registration_confirm', kwargs={'otc': reg_try.otc}))
        return render(request, self.template_name, {'form': form})


class RegistrationConfirmView(View):
    template_name = 'registration_confirm.html'

    def get(self, request, otc, *args, **kwargs):
        form = UserRegistrationForm

        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)


