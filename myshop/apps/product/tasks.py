from celery import shared_task
from .models import FileImport, Product, Brand
from .utils import parse_xlsx_file
from .admin import is_approved, is_rejected


@shared_task
def process_import_task(file_import_id):
    try:
        file_import = FileImport.objects.get(id=file_import_id)

        product_data_list = parse_xlsx_file(file_import.path)

        file_import = FileImport.objects.create(
            approved=0,
            rejected=0,
            recorded=0,
        )

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

        file_import.status = 'completed'
        file_import.save()

    except Exception as e:
        file_import.status = 'failed'
        file_import.save()
        raise e
