from django.urls import path

from apps.product.views import ProductsView, BrandView
from apps.product.views import product_by_id as product_pk_view
from apps.product.views import brand_by_id as brand_pk_view


urlpatterns = [
    path('product/', ProductsView.as_view(), name='products'),
    path('brand/', BrandView.as_view(), name='brands'),
    path('product/<int:product_id>/', product_pk_view, name='product'),
    path('brand/<int:brand_id>/', brand_pk_view, name='brand'),
]
