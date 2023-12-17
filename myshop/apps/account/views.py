from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from .forms import RegTryForm, ConfirmRegistrationForm
from .models import RegTry


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        form = RegTryForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = RegTryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user, created = User.objects.get_or_create(username=email, email=email)
            regtry = RegTry.objects.create(email=email, user=user)
            return redirect('confirm_registration', otc=regtry.otc)

        context = {'form': form}
        return render(request, self.template_name, context=context)


class ConfirmRegistrationView(View):
    template_name = 'confirm_registration.html'

    def get(self, request, otc):
        form = ConfirmRegistrationForm()

        reg_try = get_object_or_404(RegTry, otc=otc, user_id__isnull=True)

        context = {
            'otc': reg_try.otc,
            'form': form,
        }
        return render(request, self.template_name, context=context)
