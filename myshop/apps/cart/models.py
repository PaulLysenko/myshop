from django.db import models
from django.contrib.auth.models import User


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveSmallIntegerField(default=1)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items')

    @property
    def item_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    def __str__(self):
        return f'{str(self.product)} - {self.quantity} - {str(self.cart)}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    finalizing_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{str(self.user)} - {self.creation_time}: {self.finalizing_time}'

    @property
    def total_price(self):
        items_qs = self.items.all().select_related('product')
        total = 0

        for item in items_qs:
            total += item.product.price * item.quantity

        return total

    @property
    def total_amount(self):
        amount = sum([item.quantity for item in self.items.all()])
        return amount
