from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.storage import default_storage
from django import forms
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404

from apps.account.models import RegTry, UserTwoFactorAuthData
from apps.account.forms import RegTryForm, ValidateRegTryForm, LoginForm
from apps.account.tasks import send_email_task, process_registration_task


def auth2required(view_method):
    @login_required(login_url="/registration/login/")
    def wrapper(request, *args, **kwargs):
        try:
            request.user.two_factor_auth
            return Auth2View().preform_auth_2(request, target_view_method=view_method, *args, **kwargs)
        except: #request.user.two_factor_auth.RelatedObjectDoesNotExist help
            messages.add_message(request, messages.ERROR, "Set up 2FA!")
            return redirect(reverse('setup-two-factor'))

    return wrapper


class Form(forms.Form):
    code = forms.CharField(required=True)
    token = forms.CharField(required=True, widget=forms.HiddenInput())

    def clean_code(self):
        value = str(self.cleaned_data['code']).strip()

        if len(value) < 6 or not value.isdigit():
            raise forms.ValidationError('Should be 6 digits!', 'invalid')

        return value


class Auth2View(View):
    _store = {}
    template_name = "auth2code.html"
    attempts = 3

    def preform_auth_2(self, request, *args, target_view_method=None, **kwargs):
        token = str(uuid4())
        self._store[request.user.id] = {
            token: {
                'request': request,
                'args': args,
                'kwargs': kwargs,
                'target_view_method': target_view_method,
                'attempts': 3
            },
        }
        context = {
            'form': Form({'token': token}),
            'next': reverse('auth2confirm'),
        }
        messages.add_message(request, messages.ERROR, "2FA required!")
        response = render(request, self.template_name, context=context)
        return response

    @method_decorator(login_required(login_url="/registration/login/"))
    def post(self, request, *args, **kwargs):

        form = Form(request.POST)
        context = {
            'form': form,
            'next': reverse('auth2confirm'),
        }

        if not form.is_valid():
            return render(request, self.template_name, context=context)

        auth2fa_data = self._store.get(request.user.id, {})

        if not auth2fa_data or (token := form['token'].value()) not in auth2fa_data:
            return redirect(reverse('home'))

        # cache here
        auth2fa_obj = UserTwoFactorAuthData.objects.get(user_id=request.user.id)

        if not auth2fa_obj.validate_otp(form['code'].value()):
            self.attempts = auth2fa_data[token]['attempts']
            if self.attempts > 0:
                auth2fa_data[token]['attempts'] -= 1
                form.add_error('code', forms.ValidationError(f'Invalid 2fa code! You have {self.attempts} attempts left.', 'invalid'))
                return render(request, self.template_name, context=context)
            else:
                messages.add_message(request, messages.ERROR, "No more attempts left!")
                self._store.pop(request.user.id)
                # request.user.two_factor_auth.delete()
                return redirect(reverse('auth-logout'))

        self._store.pop(request.user.id)

        old_request = auth2fa_data[token]['request']
        target_view_method = auth2fa_data[token]['target_view_method']
        args = auth2fa_data[token]['args']
        kwargs = auth2fa_data[token]['kwargs']

        old_request._messages = default_storage(old_request)
        messages.add_message(old_request, messages.SUCCESS, "2FA passed!")

        return target_view_method(old_request, *args, **kwargs)


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

        if request.POST.get('next'):
            return redirect(request.POST.get('next'))

        return redirect(reverse('home'))


class LogoutView(View):

    def get(self, request):

        if request.user:
            logout(request)

        return redirect(reverse('home'))


class SetupTwoFactorAuthView(TemplateView):
    template_name = "setup_2fa.html"

    @method_decorator(login_required(login_url='/registration/login/')) #why?
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
        else:
            messages.add_message(request, messages.ERROR, "You already have 2FA!")
            return redirect(reverse('home'))

        return self.render_to_response(context)
