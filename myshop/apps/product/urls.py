from django.urls import re_path
from apps.product.views import product_by_id as product_pk_view
from apps.product.views import ProductsView

urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^(?P<product_id>\d+)$', product_pk_view, name='product'),
]
