from django.urls import re_path
from apps.brand.views import BrandView
from apps.brand.views import brand_by_id as brand_pk_view


urlpatterns = [
    re_path(r'^$', BrandView.as_view(), name='brands'),
    re_path(r'^(?P<brand_id>\d+)$', brand_pk_view, name='brand'),
]