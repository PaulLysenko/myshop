from django.urls import re_path

from .views import RegTryView
from .views import RegistrationConfirmView


urlpatterns = [
    re_path('^$', RegTryView.as_view(), name='registration'),
    re_path('^(?P<otc>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', RegistrationConfirmView.as_view(), name='registration_confirm'),
]
