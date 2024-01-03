from django.shortcuts import render, redirect

from apps.cart.forms import AddToCartForm
from apps.cart.models import Cart, CartItem


class AddToCartView:

    def view_cart(request):
        cart = Cart.objects.get(user=request.user)
        return render(request, 'cart/view_cart.html', {'cart': cart})

    def post(request, product_name, price):
        cart = Cart.objects.get(user=request.user)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(product_name=product_name, price=price)
            cart_item.quantity += quantity
            cart_item.save()
            cart.items.add(cart_item)
            return redirect('view_cart')

        return render(request, 'cart/add_to_cart.html', {'form': form, 'product_name': product_name, 'price': price})

# view for cart. get + update (delete item)
