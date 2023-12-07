from django.db import models

class Brand(models.Model):
    brand_name = models.CharField(max_length=128)
    brand_country = models.CharField(max_length=256)
    brand_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.brand_country}: {self.brand_name}'

