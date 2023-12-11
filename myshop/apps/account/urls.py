from django.urls import re_path, path

from apps.account.views import RegTryView, ValidateRegTryView

urlpatterns = [
    re_path(r'^$', RegTryView.as_view(), name='registration_try'),
    re_path(r'^(?P<otc>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
            ValidateRegTryView.as_view(), name='validate_registration')

]
