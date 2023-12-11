from django import forms

from django.core.validators import EmailValidator


class RegTryForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter exact name or exact price or partial description here ...',
                'class': 'form-control',
            },
        ),
        validators=[EmailValidator(message='Email invalid')]
    )


class ValidateRegTryForm(forms.Form):
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
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password again',
                'class': 'form-control',
            },
        ),
        required=True,
    )
