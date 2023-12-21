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


class ValidateRegTryForm(forms.Form):
    first_name = forms.CharField(
        max_length=70,
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
        max_length=70,
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
                'placeholder': 'Confirm your password',
                'class': 'form-control',
            },
        ),
        required=True,
    )

    def clean(self):
        self.cleaned_data = super().clean()
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password2']

        if pass1 != pass2:
            raise forms.ValidationError({'password': 'Passwords must be the same!'})

        return self.cleaned_data
