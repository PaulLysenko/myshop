import logging
#from django.core.exceptions import ValidationError
#from product.forms import ProductSchema


import pandas
from django.forms import ModelForm

from apps.product.bl import normalise_dataframe

ModelForm
from celery_app import celery_app

from apps.product.constants import FileImportStatus
from apps.product.models import Product, Brand, FileImport
from apps.product.product_schemas import ProductSchema
#from apps.product.forms import ProductValidationForm


logger = logging.getLogger(__name__)


@celery_app.task
def saving_product_list_task(file_import_id):
    file_import = FileImport.objects.get(id=file_import_id)
    try:
        pd_dataframe = pandas.read_excel(file_import.file_path)
    except Exception as e:
        file_import.errors.append({
            'error': repr(e)
        })
        file_import.status = FileImportStatus.ERROR
        file_import.save()
        return

    required_file_headers = set(ProductSchema.model_fields.keys())

    pd_dataframe = normalise_dataframe(pd_dataframe, required_file_headers)

    for required_header in required_file_headers:
        if required_header not in pd_dataframe:
            file_import.errors.append({
                'error': f'missed header [{required_header}]',
            })
            file_import.status = FileImportStatus.ERROR
            file_import.save()

    if file_import.errors:
        return

    # form example
    # class ProductValidationForm(ModelForm):
    #     class Meta:
    #         model = Product
    #         fields = ['name', 'price', 'description']

    # def validate_product_data_list(product_data_list):
    #     errors = []
    #
    #     for product_data in product_data_list:
    #         form = ProductValidationForm(product_data)
    #
    #         if form.is_valid():
    #             validated_data = form.cleaned_data
    #             products.append(ProductSchema(**validated_data).model_dump())
    #         else:
    #
    #             errors.append({
    #                 'product_data': product_data,
    #                 'errors': form.errors,
    #             })
    #
    #     return errors, products
    #
    # product_data_list = pd_dataframe.to_dict(orient='records')
    # products = []
    #
    # validation_errors, validated_products = validate_product_data_list(product_data_list)

    def process_product_data(pd_dataframe, file_import):
        product_data_list = pd_dataframe.to_dict(orient='records')
        products = []

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

    def process_and_save_products(pd_dataframe, file_import):
        products = process_product_data(pd_dataframe, file_import)

        if file_import.status == FileImportStatus.ERROR:
            return

        for product_data in products:
            try:
                product = ProductSchema(**product_data).model_dump()

                Product.objects.update_or_create(
                    name=product['name'],
                    defaults={
                        'price': product['price'],
                        'description': product['description'],
                        'brand': Brand.objects.filter(
                            name__iexact=product['brand'].lower(),
                        ).last() or None,
                    },
                )
            except Exception as e:
                file_import.errors.append({
                    'error': repr(e),
                })
                file_import.status = FileImportStatus.ERROR
                file_import.save()

        if file_import.status == FileImportStatus.ERROR:
            for error in file_import.errors:
                print(f"Error processing product data: {error['error']}")
        else:
            print("Products processed and saved successfully.")

    # if validation_errors:
    #     for error in validation_errors:
    #         print(f"Validation errors for product data {error['product_data']}: {error['errors']}")
    # else:
    #     print("Validated products:", validated_products)
    #
    # for product_data in products:
    #     product, created = Product.objects.update_or_create(
    #         name=product_data['name'],
    #         defaults={
    #             'price': product_data['price'],
    #             'description': product_data['description'],
    #             'brand': Brand.objects.filter(
    #                 name__iexact=product_data['brand'].lower(),
    #             ).last() or None,
    #         },
    #     )

        # if created:
        #     file_import.quantity_new += 1
        # else:
        #     file_import.quantity_updated += 1

    if not file_import.errors:
        file_import.status = FileImportStatus.SUCCESS
    else:
        file_import.status = FileImportStatus.ERROR
    file_import.save()
