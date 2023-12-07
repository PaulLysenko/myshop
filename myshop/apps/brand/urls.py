from django.urls import re_path
from apps.brand.views import BrandView
from apps.brand.views import BrandByIdView


urlpatterns = [
    re_path(r'^$', BrandView.as_view(), name='brands'),
    re_path(r'^(?P<brand_id>\d+)$', BrandByIdView.as_view(), name='brand'),
]