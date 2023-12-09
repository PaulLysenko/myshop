from django.contrib import admin
from apps.product.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'description']


admin.site.register(Brand, BrandAdmin)
