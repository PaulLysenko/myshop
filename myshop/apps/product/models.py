from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_created=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.price}'

