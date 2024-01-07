from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.cart.forms import CartForm
from apps.cart.models import Cart, CartItem


class CartView(View):
    template_name = 'cart.html'

    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)
        context = {
            'cart': cart,
        }

        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        form = CartForm(request.POST)
        context = {
            'cart': cart,
            'form': form,
        }

        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']

            cart, created = Cart.objects.get_or_create(user=request.user)

            product = CartItem.objects.get(pk=product_id)

            cart_item, created = cart.items.get_or_create(product=product)

            if not created:
                for item in cart:
                    item['update_quantity_form'] = CartForm(initial={'quantity': item['quantity'],
                                                                     'update': True})
                    cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.price = product.price
                cart_item.save()

            cart.calculate_total_price()

            product = get_object_or_404(cart_item)
            cart.remove(product)

            response = render(request, self.template_name, context=context)
            return response

        response = render(request, self.template_name, {'cart': cart})
        return response
