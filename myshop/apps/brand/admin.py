from django.contrib import admin
from apps.product.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'brand_country', 'brand_description']


admin.site.register(Brand, BrandAdmin)
