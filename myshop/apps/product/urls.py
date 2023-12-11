from django.urls import re_path

from apps.product.views import ProductsView, BrandsView


urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^(?P<product_id>\d+)$', ProductsView.as_view(), name='product'),
    re_path(r'brands/$', BrandsView.as_view(), name='brands'),
    re_path(r'brand/(?P<brand_name>\w+)$', BrandsView.as_view(), name='brand'),
]
