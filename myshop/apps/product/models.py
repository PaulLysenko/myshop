from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=99)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: {self.price}'


def error_list_default():
    return []


class FileImport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user')
    creation_time = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=256, unique=True)
    quantity_new = models.PositiveIntegerField(default=0)
    quantity_updated = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=0)     #  0: New, 10: Success, 20: Error (enum)
    errors = models.JSONField(default=error_list_default)

    def __str__(self):
        return f'{str(self.user)}: {self.file_path} - {self.creation_time.strftime("%d-%m-%Y %H:%M:%S")}'
