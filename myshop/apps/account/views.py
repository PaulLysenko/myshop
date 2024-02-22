from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.storage import default_storage

from apps.account.models import RegTry, UserTwoFactorAuthData
from apps.account.forms import RegTryForm, ValidateRegTryForm, LoginForm
from apps.account.tasks import send_email_task, process_registration_task


def auth2required(foo):
    def wrapper(request, *args, **kwargs):
        return Auth2View().get(request, target_view=foo, *args, **kwargs)

    return wrapper


class Form(forms.Form):
    code = forms.CharField(required=True)

    def clean_code(self):
        value = str(self.cleaned_data['code']).strip()

        if len(value) < 6 or not value.isdigit():
            raise forms.ValidationError('Should be 6 digits!', 'invalid')
        return value


class Auth2View(View):
    _store = {}
    template_name = "auth2code.html"

    @method_decorator(login_required)
    def get(self, request, *args, target_view=None, **kwargs):

        self._store[request.user.id] = {
            'request': request,
            'args': args,
            'kwargs': kwargs,
            'target_view': target_view,
        }
        context = {
            'form': Form(),
            'next': reverse('auth2confirm'),
        }
        messages.add_message(request, messages.ERROR, "2FA required!")
        response = render(request, self.template_name, context=context)
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        form = Form(request.POST)
        context = {
            'form': form,
            'next': reverse('auth2confirm'),
        }

        if not form.is_valid():
            return render(request, self.template_name, context=context)

        auth2fa_data = self._store.get(request.user.id)
        if not auth2fa_data:
            return redirect(reverse('home'))

        auth2fa_obj = UserTwoFactorAuthData.objects.get(user_id=request.user.id)

        if not auth2fa_obj.validate_otp(form['code'].value()):
            form.add_error('code', forms.ValidationError('Invalid 2fa code, try again.', 'invalid'))
            return render(request, self.template_name, context=context)

        old_request = auth2fa_data['request']
        target_view = auth2fa_data['target_view']
        args = auth2fa_data['args']
        kwargs = auth2fa_data['kwargs']

        old_request._messages = default_storage(old_request)
        messages.add_message(old_request, messages.SUCCESS, "2FA passed!")

        return target_view(old_request, *args, *kwargs)


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


class SetupTwoFactorAuthView(TemplateView):
    template_name = "setup_2fa.html"

    def post(self, request):
        context = {}
        user = request.user

        user2fa_data, created = UserTwoFactorAuthData.objects.get_or_create(user=user)
        context["is_created"] = created

        if created:
            context["otp_secret"] = user2fa_data.gauth_secret
            context["qr_code"] = user2fa_data.generate_qr_code(
                name=user.email,
            )

        return self.render_to_response(context)

