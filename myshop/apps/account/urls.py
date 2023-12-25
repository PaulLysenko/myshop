from django.urls import re_path
from apps.account.views import RegTryView, ValidateRegTryView, LoginView, LogoutView

urlpatterns = [
    re_path(r'^$', RegTryView.as_view(), name='registration_try'),
    re_path(r'^login$', LoginView.as_view(), name='auth-login'),
    re_path(r'^logout$', LogoutView.as_view(), name='auth-logout'),
    re_path(r'^(?P<otc>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
            ValidateRegTryView.as_view(), name='validate_registration_try'),
]
