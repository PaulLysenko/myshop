from django.urls import path, re_path

from apps.cart.views import CartView, AddCartView

urlpatterns = [
    path('', CartView.as_view(), name='view_cart'),
    re_path(r'^add/(?P<product_id>\d+)', AddCartView.as_view(), name='add_to_cart'),
]
