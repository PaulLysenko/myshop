from datetime import datetime

from django.conf import settings

from apps.product.constants import IMPORTED_FILE_PATH, FileImportStatus
from apps.product.forms import ProductValidationForm
from apps.product.models import FileImport, Product
from apps.product.product_schemas import ProductSchema


def save_file_to_storage(imported_file):
    file_path = IMPORTED_FILE_PATH.format(datetime.now().strftime("%Y_%m_%d-%H_%M_%S"), imported_file.name)
    abs_file_path = str(settings.BASE_DIR) + file_path
    # save imported file to the hard drive
    with open(abs_file_path, 'wb') as saved_file:
        saved_file.write(imported_file.read())

    return file_path


def normalise_dataframe(pd_dataframe, required_file_headers):
    for header in pd_dataframe:
        new_header = header.lower().strip()
        if new_header != header and new_header in required_file_headers:
            pd_dataframe.insert(0, new_header, getattr(pd_dataframe, header))

        if header not in required_file_headers:
            pd_dataframe.drop(header, axis=1, inplace=True)

    return pd_dataframe


def schema_product_data_validation(product_data_list, products, file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)

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
    return products


def form_product_data_validation(product_data_list, products, file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)

    for product in product_data_list:
        try:
            product_object = Product.objects.filter(name=product['name']).last()
            if product_object:
                form = ProductValidationForm(product, instance=product_object)
                products.append(product)
                form.save()
            else:
                form = ProductValidationForm(product)
                if form.is_valid():
                    products.append(product)
                    form.save()
                else:
                    file_import.errors.append({
                        'error': form.errors,
                    })
                    file_import.status = FileImportStatus.ERROR
                    file_import.save()
        except Exception as e:
            file_import.errors.append({
                'error': repr(e),
            })
            file_import.status = FileImportStatus.ERROR
            file_import.save()
            continue
    return products
