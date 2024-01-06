from django.urls import re_path

from apps.cart.views import CartView

urlpatterns = [
    re_path(r'^$', CartView.as_view(), name='cart')
]
