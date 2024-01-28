import logging

import pandas

from celery_app import celery_app

from apps.product.models import Product, Brand, FileImport


logger = logging.getLogger(__name__)


@celery_app.task
def saving_product_list_task(file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)
    try:
        pd_dataframe = pandas.read_excel(file_import.file_path)
        # check headers
        # normalize data
        product_data_list = pd_dataframe.to_dict(orient='records')
    except Exception as e:
        file_import.errors.append({
            'error': e
        })

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
        if created:
            file_import.quantity_new += 1
        else:
            file_import.quantity_updated += 1

    file_import.save()
