from django.urls import re_path

from apps.product.views import ProductsView, BrandsView


urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^(?P<product_id>\d+)$', ProductsView.product_by_id, name='product'),
    re_path(r'brands/$', BrandsView.as_view(), name='brands'),
    re_path(r'brand/(?P<brand_name>\w+)$', BrandsView.brand_by_name, name='brand'),
]
