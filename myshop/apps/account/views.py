from django.contrib.auth.models import User
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.account.models import RegTry
from apps.account.forms import RegTryForm, ValidateRegTryForm, LoginForm
from apps.account.tasks import send_email_task, process_registration_task


class RegTryView(View):
    template_name = 'registration_try.html'

    def get(self, request):
        form = RegTryForm()
        context = {'form': form}
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

        send_email_task.delay(otc=reg_try.otc, email=reg_try.email)

        messages.add_message(request, messages.INFO, f"Please check our email")
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

        process_registration_task.delay(form.cleaned_data, reg_try.id)

        return redirect(reverse('home'))


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        email_value = form.cleaned_data['email']
        password_value = form.cleaned_data['password']

        try:
            username = User.objects.get(email=email_value.lower()).username
        except User.DoesNotExist:
            form.add_error(None, 'Incorrect login or password')
            return render(request, self.template_name, {'form': form})

        user = authenticate(username=username, password=password_value)

        if not user:
            form.add_error(None, 'Incorrect login or password')
            return render(request, self.template_name, {'form': form})

        login(request, user)

        return redirect(reverse('home'))


class LogoutView(View):

    def get(self, request):

        if request.user:
            logout(request)

        return redirect(reverse('home'))
