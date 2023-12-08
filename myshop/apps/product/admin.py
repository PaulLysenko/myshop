from django.contrib import admin
from apps.product.models import Product
from apps.product.models import Brand


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']


admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'description']


admin.site.register(Brand, BrandAdmin)
