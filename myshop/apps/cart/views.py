from django.shortcuts import render, redirect

from apps.cart.forms import Form
from apps.cart.models import Cart, CartItem
from django.views import View


# TODO: add_to_cart_view
# view for adding product into cart by id and quantity
# user -> cart (get or create)
# product_id, quantity -> create cart_item
# cart_item -> cart

class CartView(View):
    def view_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        return render(request, 'cart/view_cart.html', {'cart': cart})

    def post(request, product_name, price):
        cart = Cart.objects.get(user=request.user)
        form = Form(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(product_name=product_name, price=price)
            cart_item.quantity += quantity
            cart_item.save()
            cart.items.add(cart_item)
            return redirect('view_cart')

        return render(request, 'cart/view_cart.html', {'form': form, 'product_name': product_name, 'price': price})

# view for cart. get + update (delete item)
