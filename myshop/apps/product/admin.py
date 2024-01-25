from django.contrib import admin
from django.urls import re_path
from django.shortcuts import render
from django.contrib import messages

from apps.product.forms import ProductImportForm
from apps.product.models import Product, Brand, FileImport
from apps.product.bl import save_file_to_storage, parse_xlsx_file
from apps.product.tasks import saving_product_list_task


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

                path = save_file_to_storage(file)

                file_import = FileImport.objects.create(user=request.user, file_path=path, )

                # get file_import by id

                product_data_list = parse_xlsx_file(path)

                file_import.count_new(product_data_list=product_data_list)

                saving_product_list_task.delay(product_data_list=product_data_list)

                # todo: use messages with result

                messages.add_message(request, messages.SUCCESS, f"""Success! 
                {file_import.quantity_new} new products were added
                {file_import.quantity_updated} old products were updated""")

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


@admin.register(FileImport)
class FileImportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
