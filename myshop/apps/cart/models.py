from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='items')
    creation_time = models.DateTimeField(auto_now=True, auto_created=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)  # recalculate
    close_time = models.DateTimeField(auto_now=True, auto_created=True)

    def calculate_total_price(self):
        total_price = self.objects.annotate(
            total_price=Sum(F('price') * F('quantity'))
        )['total_price'] or 0

        self.total_price = total_price
        self.save()
