from django import forms
from django.core.validators import EmailValidator


class RegTryForm(forms.Form):
    email = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control',
            },
        ),
        validators=[EmailValidator(message='Enter a valid email address.')]
    )


class ConfirmRegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your first name',
                'class': 'form-control',
            },
        ),
        required=True,
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your last name',
                'class': 'form-control',
            },
        ),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'form-control',
            },
        ),
        required=True,
    )
