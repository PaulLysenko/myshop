from django.contrib import admin
from django.urls import re_path
from django.shortcuts import render

from apps.product.forms import ProductImportForm
from apps.product.models import Product
from apps.product.models import Brand


def handle_file(file):
    # todo: parse file (pandas)
    # todo: check headers
    # todo: get data
    # todo: save data into DB into products
    # todo: return result message 'success' or errors

    # name(str),   brand(select id by name)  price(decimal), description(text),
    # Iphone       Apple                     100500.99       blablabla

    return 'success'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'price', 'brand']

    @staticmethod
    def import_products_view(request):
        result = ''
        form = ProductImportForm()

        if request.method == 'POST':
            form = ProductImportForm(files=request.FILES)
            if form.is_valid():
                file = form.cleaned_data["file"]
                result = handle_file(file)
                # todo: use messages with result

        return render(request, 'admin/product/product_import.html', {'form': form, 'result': result})

    def get_urls(self):
        urls = super().get_urls()
        urls.append(
            re_path(
                r"import_file",
                self.admin_site.admin_view(self.import_products_view),
                name='import_product_file',
            )
        )

        return urls


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
