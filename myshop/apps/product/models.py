from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}: {self.price}'
