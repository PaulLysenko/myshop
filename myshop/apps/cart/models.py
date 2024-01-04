from django.db import models
from django.contrib.auth.models import User


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items')
    creation_time = models.DateTimeField(auto_now_add=True)
    finalizing_time = models.DateTimeField(null=True, blank=True)
    # todo: creation time



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)  # recalculate
    # todo: finalizing time
