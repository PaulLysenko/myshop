from django.views import View
from django.shortcuts import render, redirect

from apps.cart.models import Cart, CartItem
from apps.product.models import Product


class CartView(View):
    template = 'view_cart.html'

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(
            user_id=request.user.id,
            finalizing_time__isnull=True,
        )

        return render(request, self.template, context={'cart': cart})


class AddCartView(View):
    template = 'view_cart.html'

    def post(self, request, product_id):
        cart, _created = Cart.objects.get_or_create(
            user_id=request.user.id,
            finalizing_time__isnull=True,
        )

        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            product_id=product.id,
            cart_id=cart.id,
            defaults={
                'quantity': 1,
                'price': product.price,
            }
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('view_cart')
