from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RegTry


class RegTryForm(forms.ModelForm):

    class Meta:
        model = RegTry
        fields = ['email']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = RegTry
        fields = ('email', 'password1', 'password2')