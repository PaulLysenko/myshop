from django.urls import path
from apps.cart.views import AddToCartView

urlpatterns = [
    path('cart/', AddToCartView.view_cart(), name='view_cart'),]
