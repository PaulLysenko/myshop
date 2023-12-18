from django.urls import re_path

from apps.account.views import RegTryView, RegTryConfirmationView


urlpatterns = [
    re_path(r'^$', RegTryView.as_view(), name='reg_try'),
    re_path('^(?P<otc>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', RegTryConfirmationView.as_view(), name='reg_try_confirm')
    # re_path(r'^brand/$', BrandsView.as_view(), name='brands'),
    # re_path(r'^(?P<product_id>\d+)$', product_pk_view, name='product'),
    # re_path(r'^brand/(?P<brand_id>\d+)/$', BrandDetailView.as_view(), name='brand'),
]
