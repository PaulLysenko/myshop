from django.db import models


class ProductBrand(models.Model):

    brand_name = models.CharField(max_length=100)
    brand_origin_country = models.CharField(max_length=50)
    brand_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):

    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.price}'

    class Meta:
        ordering = ['name']
