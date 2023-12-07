from django.db import models

# Create your models here.
class Brand(models.Model):

    name_brand = models.CharField(max_length=128)
    country_brand = models.CharField(max_length=256)
    description_brand = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name_brand}: {self.country_brand}'