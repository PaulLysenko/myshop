import logging

from celery_app import celery_app
from apps.product.models import Product, Brand


logger = logging.getLogger(__name__)


@celery_app.task
def saving_product_list_task(product_data_list):
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
