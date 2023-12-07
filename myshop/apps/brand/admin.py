from django.contrib import admin
from apps.brand.models import Brand



class BrandAdmin(admin.ModelAdmin):
    list_display = ['name_brand', 'country_brand', 'description_brand']


admin.site.register(Brand, BrandAdmin)
# Register your models here.
