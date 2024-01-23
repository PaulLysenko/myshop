from django.contrib import admin
from django.urls import re_path
from django.shortcuts import render
from django.contrib import messages
import datetime

from apps.product.forms import ProductImportForm
from apps.product.models import Product
from apps.product.models import Brand
from apps.product.bl import save_file_to_storage, parse_xlsx_file
from .models import FileImport


def is_approved(product_data):
    return product_data.get('approved', 0)

def is_rejected(product_data):
    return product_data.get('rejected', 0)


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

                current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"import_file_{current_time}.xlsx"

                path = save_file_to_storage(file)

                # get file_import by id

                product_data_list = parse_xlsx_file(path)

                file_import = FileImport.objects.create(
                    approved=0,
                    rejected=0,
                    recorded=0,
                )

                # validate data

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

                file_import.approved = len(
                    [product_data for product_data in product_data_list if is_approved(product_data)])
                file_import.rejected = len(
                    [product_data for product_data in product_data_list if is_rejected(product_data)])
                file_import.recorded = len(product_data_list) - file_import.approved - file_import.rejected
                file_import.save()

                # save result info into file_import

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


class FileImportAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'approved', 'rejected', 'recorded']

admin.site.register(FileImport, FileImportAdmin)
