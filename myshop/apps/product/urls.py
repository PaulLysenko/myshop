from django.urls import path
from apps.product.views import product as product_view


urlpatterns = [
    path('', product_view),
]
