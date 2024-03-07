from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

from apps.product.constants import (
    FileImportStatus,
    DEFAULT_PRODUCT_CACHE_TIME,
    DEFAULT_PRODUCT_ALL_CACHE_KEY,
)


class CashedProductsManager(models.Manager):
    def all(self):

        qs = cache.get(
            key=DEFAULT_PRODUCT_ALL_CACHE_KEY,
            default=Product.objects.none(),
        )
        if not qs.exists():
            qs = super().all()
            cache.set(
                key=DEFAULT_PRODUCT_ALL_CACHE_KEY,
                value=qs,
                timeout=DEFAULT_PRODUCT_CACHE_TIME,
            )

        return qs


# class CashedProductsQuerySet(models.QuerySet):
#     def cashed(self):
#         qs = cache.get(
#             key=DEFAULT_PRODUCT_ALL_CACHE_KEY,
#             default=Product.objects.none(),
#         )
#         if not qs.exists():
#             qs = super().all()
#             cache.set(
#                 key=DEFAULT_PRODUCT_ALL_CACHE_KEY,
#                 value=qs,
#                 timeout=DEFAULT_PRODUCT_CACHE_TIME,
#             )
#
#         return qs


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=99, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.Manager()
    cashed_objects = CashedProductsManager()
    # cashed_objects = CashedProductsQuerySet.as_manager()

    name = models.CharField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
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
    status = models.PositiveSmallIntegerField(default=FileImportStatus.NEW, choices=FileImportStatus.choices())
    errors = models.JSONField(default=error_list_default)

    def __str__(self):
        return f'{str(self.user)}: {self.file_path} - {self.creation_time.strftime("%d-%m-%Y %H:%M:%S")}'
