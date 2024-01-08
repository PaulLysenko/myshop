import uuid

from django.db import models
from django.contrib.auth.models import User


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='product_items')
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    creation_time = models.DateTimeField(auto_now=True)
    # todo: creation time

    def get_item_price(self):
        self.price = self.product.price * self.quantity
        self.save()
        return self.price

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    ref_code = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)  # recalculate
    finalizing_time = models.DateTimeField(auto_now=True)
    # todo: finalizing time

    @property
    def get_amount(self):
        amount = sum([item.quantity for item in self.items.all()])
        return amount

    def get_total_price(self):
        total_price = sum([item.price for item in self.items.all()])
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f'{self.user} - {self.ref_code}'

