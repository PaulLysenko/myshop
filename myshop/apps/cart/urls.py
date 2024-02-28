from django.urls import path, re_path

from apps.cart.views import CartView, AddCartView, RemoveFromCartView
from apps.account.views import SetupTwoFactorAuthView

urlpatterns = [
    path('', CartView.as_view(), name='view_cart'),
    re_path(r'^add/(?P<product_id>\d+)', AddCartView.as_view(), name='add_to_cart'),
    re_path(r'^remove/(?P<cart_item_id>\d+)', RemoveFromCartView.as_view(), name='remove_from_cart'),
    re_path(r'^verification/(?P<product_id>\d+)', SetupTwoFactorAuthView.as_view(), name='verification'),
]
