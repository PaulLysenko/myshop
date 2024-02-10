from datetime import datetime
from pathlib import PurePath

from django.conf import settings

from apps.product.constants import IMPORTED_FILE_NAME, FileImportStatus, IMPORTED_FILE_DIRECTORY
from apps.product.forms import ProductValidationForm
from apps.product.models import FileImport, Product, Brand
from apps.product.product_schemas import ProductSchema


def save_file_to_storage(imported_file):
    file_name = IMPORTED_FILE_NAME.format(datetime.now().strftime("%Y_%m_%d-%H_%M_%S"), imported_file.name)
    abs_file_path = PurePath(settings.BASE_DIR, IMPORTED_FILE_DIRECTORY, file_name)

    # save imported file to the hard drive
    with open(abs_file_path, 'wb') as saved_file:
        saved_file.write(imported_file.read())

    return file_name


def normalise_dataframe(pd_dataframe, required_file_headers):
    for header in pd_dataframe:
        new_header = header.lower().strip()
        if new_header != header and new_header in required_file_headers:
            pd_dataframe.insert(0, new_header, getattr(pd_dataframe, header))

        if header not in required_file_headers:
            pd_dataframe.drop(header, axis=1, inplace=True)

    return pd_dataframe


def schema_product_data_validation(product_data_list, file_import_id):
    file_import = FileImport.objects.filter(id=file_import_id, status=FileImportStatus.NEW).last()
    products: list[dict] = []
    for product in product_data_list:
        try:
            products.append(ProductSchema(**product).model_dump())
        except Exception as e:
            file_import.errors.append({
                'error': repr(e),
            })
            file_import.status = FileImportStatus.ERROR
            file_import.save()
            continue

    for product_data in products:
        product, created = Product.objects.update_or_create(
            name=product_data['name'],
            defaults={
                'price': product_data['price'],
                'description': product_data['description'],
                'brand': Brand.objects.filter(
                    name__iexact=product_data['brand'].lower(),
                ).last() or None,
            },
        )

        if created:
            file_import.quantity_new += 1
        else:
            file_import.quantity_updated += 1

    if not file_import.errors:
        file_import.status = FileImportStatus.SUCCESS
    file_import.save()
    return products


def form_product_data_validation(product_data_list, file_import_id):
    file_import = FileImport.objects.filter(id=file_import_id, status=FileImportStatus.NEW).last()
    products: list[dict] = []
    for product in product_data_list:
        product_object = Product.objects.filter(name__iexact=product['name'].lower()).last()
        # Brand.objects.filter(name__iexact=product['brand'].lower()).last() or None,
        try:
            product_brand, created = Brand.objects.get_or_create(name=product['brand'].title()) or None
            product['brand'] = product_brand.id if product_brand else None
        except Exception as e:
            file_import.errors.append({
                'error': repr(e),
            })
        # try:
        #     product_brand = Brand.objects.filter(name__iexact=product['brand'].lower()).last()
        #     product['brand'] = product_brand.name
        # except Exception:
        #     product_brand = Brand.objects.create(name=product['brand'])
        #     product['brand'] = product_brand.name
        form = ProductValidationForm(product, instance=product_object)
        if form.is_valid():
            products.append(form.cleaned_data)
            form.save()
            if product_object:
                file_import.quantity_updated += 1
            else:
                file_import.quantity_new += 1
        else:
            file_import.errors.append({
                'error': form.errors,
            })
            file_import.status = FileImportStatus.ERROR
        file_import.save()
    if not file_import.errors:
        file_import.status = FileImportStatus.SUCCESS
    file_import.save()
    return products
