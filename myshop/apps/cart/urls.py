from django.urls import re_path

from apps.cart.views import CartView

urlpatterns = [
    re_path(r'^$', CartView.as_view(), name='cart'),
    re_path(r'^add-to-cart/(?P<product_id>\d+)/$', CartView.as_view(), name='add_to_cart'),
]
