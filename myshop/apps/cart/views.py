from django.shortcuts import render, redirect

from apps.cart.models import Cart, CartItem


class AddToCartView:

    def view_cart(request):
        cart = Cart.objects.get(user=request.user)
        return render(request, 'cart/view_cart.html', {'cart': cart})

    def add_to_cart(request, product_name, price):
        cart = Cart.objects.get(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(product_name=product_name, price=price)
        cart.items.add(cart_item)
        return redirect('view_cart')

# view for cart. get + update (delete item)
