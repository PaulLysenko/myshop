from django.urls import re_path, include

from apps.product.views import product_by_id as product_pk_view
from apps.product.views import ProductsView
from apps.product.views import BrandsView
from apps.product.views import BrandDetailView

urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^brand/$', BrandsView.as_view(), name='brands'),
    re_path(r'^(?P<product_id>\d+)$', product_pk_view, name='product'),
    re_path(r'^brand/(?P<brand_id>\d+)/$', BrandDetailView.as_view(), name='brand'),
]

