import logging

import pandas

from django.conf import settings

from celery_app import celery_app

from apps.product.bl import normalise_dataframe, schema_product_data_validation, form_product_data_validation
from apps.product.constants import FileImportStatus
from apps.product.models import Product, Brand, FileImport
from apps.product.product_schemas import ProductSchema


logger = logging.getLogger(__name__)


@celery_app.task
def saving_product_list_task(file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)
    file_path = str(settings.BASE_DIR) + file_import.file_path
    try:
        pd_dataframe = pandas.read_excel(file_path)
    except Exception as e:
        file_import.errors.append({
            'error': repr(e)
        })
        file_import.status = FileImportStatus.ERROR
        file_import.save()
        return

    required_file_headers = set(ProductSchema.model_fields.keys())

    normalized_pd_dataframe = normalise_dataframe(pd_dataframe, required_file_headers)

    for required_header in required_file_headers:
        if required_header not in normalized_pd_dataframe:
            file_import.errors.append({
                'error': f'missed header [{required_header}]',
            })
            file_import.status = FileImportStatus.ERROR
            file_import.save()

    if file_import.errors:
        return

    product_data_list: list[dict] = normalized_pd_dataframe.to_dict(orient='records')
    products: list[dict] = []

    # products = schema_product_data_validation(product_data_list, products, file_import_id)
    products = form_product_data_validation(product_data_list, products, file_import_id)

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
    #
    # if not file_import.errors:
    #     file_import.status = FileImportStatus.SUCCESS
    # file_import.save()
