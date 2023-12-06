from django.contrib import admin
from apps.product.models import Product, ProductBrand


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']

    raw_id_fields = ['brand']

    def brand_name(self, obj):
        if obj.brand:
            return obj.brand.brand_name
        else:
            return ''

    brand_name.description = 'Brand Name'


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductBrand)
