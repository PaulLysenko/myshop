from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=128)
    country = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.country}: {self.name}'
