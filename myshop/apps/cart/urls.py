from django.urls import path
from apps.cart.views import AddToCartView

urlpatterns = [
    path('cart/', AddToCartView.view_cart(), name='view_cart'),
    path('add_to_cart/<str:product_name>/<float:price>/', AddToCartView.add_to_cart(), name='add_to_cart'),]
