from django.contrib import admin
from django.urls import re_path
from django.shortcuts import render
from django.contrib import messages

from apps.product.forms import ProductImportForm
from apps.product.models import Product
from apps.product.models import Brand
from apps.product.bl import parse_xlsx_file, save_file_to_storage
from apps.product.tasks import parsing_file


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

                path = parsing_file(save_file_to_storage(file))

                product_data_list = parse_xlsx_file(path)

                for product_data in product_data_list:
                    product, created = Product.objects.update_or_create(
                        name=product_data['name'],
                        defaults={
                            'price': product_data['price'],
                            'description': product_data['description'],
                            'brand': Brand.objects.filter(
                                name__iexact=product_data['brand'].lower(),
                            ).last() or None,
                        }
                    )

                # save result info into file_import

                # TODO: HW <--- make celery task

                # todo: use messages with result

                messages.add_message(request, messages.ERROR, "Hello world.")

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
