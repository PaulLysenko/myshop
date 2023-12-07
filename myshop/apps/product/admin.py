from django.contrib import admin
from apps.product.models import Product



class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']


admin.site.register(Product, ProductAdmin)
