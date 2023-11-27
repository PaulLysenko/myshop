from django.urls import re_path
from apps.product.views import products_all as product_view, product_by_id as product_pk_view


urlpatterns = [
    re_path(r'^$', product_view, name='products'),
    re_path(r'(?P<product_id>\d+)', product_pk_view, name='product'),
]
