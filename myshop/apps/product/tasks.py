import logging

import pandas

from celery_app import celery_app

from apps.product.constants import FileImportStatus
from apps.product.models import Product, Brand, FileImport
from apps.product.product_schemas import ProductSchema


logger = logging.getLogger(__name__)


@celery_app.task
def saving_product_list_task(file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)
    try:
        pd_dataframe = pandas.read_excel(file_import.file_path)
    except Exception as e:
        file_import.errors.append({
            'error': e
        })
        file_import.status = FileImportStatus.ERROR
        file_import.save()
        return

    # check headers  # dataframe

    product_data_list: list[dict] = pd_dataframe.to_dict(orient='records')

    products: list[dict] = []

    for product in product_data_list:
        try:
            products.append(ProductSchema(**product).model_dump())
        except Exception as e:
            file_import.errors.append({
                'error': e,
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
            }
        )

        if created:
            file_import.quantity_new += 1
        else:
            file_import.quantity_updated += 1

    if not file_import.errors:
        file_import.status = FileImportStatus.SUCCESS
    else:
        file_import.status = FileImportStatus.ERROR
    file_import.save()
