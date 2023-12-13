from django.urls import path

from .views import registration
from .views import registration_confirm


urlpatterns = [
    path('', registration, name='registration'),
    path('<str:otc>/', registration_confirm, name='registration_confirm'),
]
