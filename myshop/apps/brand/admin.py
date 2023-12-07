from django.contrib import admin
from apps.brand.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'description']


admin.site.register(Brand, BrandAdmin)
# Register your models here.
