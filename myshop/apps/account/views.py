from django.shortcuts import render, redirect
from .forms import RegTryForm
from .models import RegTry
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm
from django.http import HttpResponse


def registration(request):
    if request.method == 'GET':
        form = RegTryForm()
        return render(request, 'RegTry.html', {'form': form})
    elif request.method == 'POST':
        form = RegTryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not RegTry.objects.filter(email=email).exists():
                reg_try = RegTry.objects.create(email=email)
                return redirect('registration_confirm', reg_try.otc)
            else:
                return render(request, 'RegTry.html', {'form': form, 'error': 'Email already registered'})
        else:
            return render(request, 'RegTry.html', {'form': form})


def registration_confirm(request, otc):
    reg_try = get_object_or_404(RegTry, otc=otc)
    if request.method == 'GET':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = reg_try.email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            reg_try.delete()
            return HttpResponse("Registration completed successfully.")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration_confirm.html', {'form': form, 'reg_try': reg_try})