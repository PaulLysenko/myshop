from django.db import models
from apps.account.models import RegTry


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=99)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: {self.price}'


class FileImport(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    approved = models.DecimalField(max_digits=10, decimal_places=2)
    recorded = models.DecimalField(max_digits=10, decimal_places=2)
    rejected = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.admin_name}:{self.created_at}:{self.approved}:{self.rejected}:{self.recorded}'

