from django.urls import re_path

from apps.api.views import ProductsApiView, ProductApiView

urlpatterns = [
    re_path(r'products/?$', ProductsApiView.as_view(), name='products'),
    re_path(r'products/(?P<pk>\d+)/?$', ProductApiView.as_view(), name='products'),
]
