from django.contrib.auth.models import User


def process_registration(form, reg_try):
    user = User.objects.create_user(
        username=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
        email=reg_try.email,
        password=form.cleaned_data['password'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
    )
    reg_try.user = user
    reg_try.save()