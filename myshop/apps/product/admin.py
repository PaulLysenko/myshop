from django.contrib import admin
from django.urls import re_path
from django.shortcuts import render
from django.contrib import messages

from apps.product.forms import ProductImportForm
from apps.product.models import Product, Brand, FileImport
from apps.product.bl import save_file_to_storage
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
                file_name = save_file_to_storage(file)
                file_import = FileImport.objects.create(user=request.user, file_path=file_name)

                # saving_product_list_task(file_import_id=file_import.id)
                saving_product_list_task.delay(file_import_id=file_import.id)

                messages.add_message(request, messages.SUCCESS, f"File Saved!")

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
