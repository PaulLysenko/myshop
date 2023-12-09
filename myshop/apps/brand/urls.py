from django.urls import re_path
from apps.brand.views import BrandView

urlpatterns = [
    re_path(r'^$', BrandView.as_view(), name='brands'),
    re_path(r'^(?P<brand_id>\d+)$', BrandView.as_view(), name='brand')
]
