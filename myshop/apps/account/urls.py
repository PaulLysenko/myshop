from django.urls import path
from apps.account.views import RegistrationView, ConfirmRegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/<str:otc>/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
]
