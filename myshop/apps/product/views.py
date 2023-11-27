from django.http import Http404
from django.shortcuts import render
from apps.product.models import Product


def products_all(request, *args, **kwargs):

    products = Product.objects.all()

    return render(request, 'product_template.html', context={'products': products})


def product_by_id(request, product_id=None, *args, **kwargs):

    products = Product.objects.filter(id=product_id)
    if not products:
        raise Http404("Product does not exist")

    return render(request, 'product_template_single_product.html', context={'product': products.last()})
