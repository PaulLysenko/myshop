from django.urls import re_path

from apps.product.views import ProductView, ProductsView, BrandsView, BrandDetailView

urlpatterns = [
    re_path(r'^$', ProductsView.as_view(), name='products'),
    re_path(r'^brands/$', BrandsView.as_view(), name='brands'),
    re_path(r'^(?P<product_id>\d+)$', ProductView.as_view(), name='product'),
    re_path(r'^brand/(?P<brand_id>\d+)/$', BrandDetailView.as_view(), name='brand'),
]
