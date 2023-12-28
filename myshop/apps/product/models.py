from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=99)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: {self.price}'
