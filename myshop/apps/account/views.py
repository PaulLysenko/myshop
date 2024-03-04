import copy
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.cache import cache
from django import forms
from django.http import HttpRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404

from apps.account.constants import MAX_ATTEMPTS_NUMBER
from apps.account.models import RegTry, UserTwoFactorAuthData
from apps.account.forms import RegTryForm, ValidateRegTryForm, LoginForm
from apps.account.tasks import send_email_task, process_registration_task


FUNCTION_MAPPING = {}


def auth2required(view_method):

    view_method_id = str(len(FUNCTION_MAPPING))
    FUNCTION_MAPPING[view_method_id] = view_method

    @login_required(login_url="/registration/login/")
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'two_factor_auth'):
            messages.add_message(request, messages.ERROR, "Set up 2FA!")
            return redirect(reverse('setup-two-factor'))
        try:
            return Auth2View().preform_auth_2(request, target_view_method_id=view_method_id, *args, **kwargs)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"{repr(e)}!")
            return redirect(reverse('home'))

    return wrapper


class Form(forms.Form):
    code = forms.CharField(required=True)
    token = forms.CharField(required=True, widget=forms.HiddenInput())

    def clean_code(self):
        value = str(self.cleaned_data['code']).strip()

        if len(value) < 6 or not value.isdigit():
            raise forms.ValidationError('Should be 6 digits!', 'invalid')

        return value


def duplicate_request(request):
    keys = ('wsgi.errors', 'wsgi.input')

    for k in keys:
        if k in request.META:
            request.META.pop(k)

    new_request = HttpRequest()

    new_request.method = request.method
    new_request.path = request.path
    new_request.META = copy.deepcopy(request.META)
    new_request.GET = copy.deepcopy(request.GET)
    new_request.POST = copy.deepcopy(request.POST)

    return new_request


class Auth2View(View):
    template_name = "auth2code.html"

    def preform_auth_2(self, request, *args, target_view_method_id, **kwargs):
        token = str(uuid4())

        cache.set(
            key=request.user.id,
            value={
                token: {
                    'request': duplicate_request(request),
                    'args': args,
                    'kwargs': kwargs,
                    'target_view_method_id': target_view_method_id,
                    'attempts': MAX_ATTEMPTS_NUMBER,
                },
            },
            timeout=5 * 60,  # 5 minutes
        )
        context = {
            'form': Form({'token': token}),
            'next': reverse('auth2confirm'),
        }

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

        auth2fa_data = cache.get(request.user.id, {})

        if not auth2fa_data or (token := form['token'].value()) not in auth2fa_data:
            return redirect(reverse('home'))

        # cache here ?
        auth2fa_obj = UserTwoFactorAuthData.objects.get(user_id=request.user.id)

        if not auth2fa_obj.validate_otp(form['code'].value()):
            if auth2fa_data[token]['attempts'] > 0:
                form.add_error('code', forms.ValidationError(f'Invalid 2fa code! You have {auth2fa_data[token]["attempts"]} attempts left.', 'invalid'))
                auth2fa_data[token]['attempts'] -= 1
                return render(request, self.template_name, context=context)
            else:
                messages.add_message(request, messages.ERROR, "No more attempts left!")
                return redirect(reverse('auth-logout'))


        old_request = auth2fa_data[token]['request']
        target_view_method = FUNCTION_MAPPING[auth2fa_data[token]['target_view_method_id']]
        args = auth2fa_data[token]['args']
        kwargs = auth2fa_data[token]['kwargs']

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

    @method_decorator(login_required(login_url='/registration/login/'))
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
