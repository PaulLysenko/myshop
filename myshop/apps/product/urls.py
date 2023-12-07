from django.urls import re_path
from apps.product.views import ProductsView, BrandView
from apps.product.views import product_by_id as product_pk_view
from apps.product.views import brand_by_id as brand_pk_view


urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^brand/$', BrandView.as_view(), name='brands'),
    re_path(r'^(?P<product_id>\d+)$', product_pk_view, name='product'),
    re_path(r'^brand/(?P<brand_id>\d+)/$', brand_pk_view, name='brand'),
]
