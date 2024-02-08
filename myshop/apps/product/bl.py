from datetime import datetime

from django.conf import settings

from apps.product.constants import IMPORTED_FILE_PATH


def save_file_to_storage(imported_file):
    file_path = IMPORTED_FILE_PATH.format(datetime.now().strftime("%Y_%m_%d-%H_%M_%S"), imported_file.name)
    abs_file_path = str(settings.BASE_DIR) + file_path
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


def validate_product_data_list(product_data_list):
    errors = []

    for product_data in product_data_list:
        form = ProductValidationForm(product_data)

        if form.is_valid():
            validated_data = form.cleaned_data
            products.append(ProductSchema(**validated_data).model_dump())
        else:

            errors.append({
                'product_data': product_data,
                'errors': form.errors,
            })

    return errors, products
