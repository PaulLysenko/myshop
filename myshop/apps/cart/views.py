from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.cart.models import CartItem, Cart
from apps.product.models import Product


class CartView(View):
    template_name = 'cart.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('auth-login'))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items =cart.items.all()
        context = {
            'cart': cart,
            'cart_items': cart_items
        }
        return render(request, self.template_name, context=context)

    def post(self, request, product_id=None):
        if not request.user.is_authenticated:
            return redirect(reverse('auth-login'))
        if not product_id:
            return HttpResponseBadRequest("Product ID is required")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseBadRequest("Invalid product id")
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.get_item_price()
        cart_item.save()
        cart.get_total_price()
        return redirect('cart')
