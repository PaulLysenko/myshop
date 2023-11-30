from django.db.models import Q
from decimal import Decimal
from django.http import Http404
from django.shortcuts import render
from apps.product.models import Product


def products_all(request, *args, **kwargs):

    products = Product.objects.all()

    if request.method == 'POST':

        search_value = request.POST['search'].strip()

        if search_value:
            query = Q(name=search_value) | Q(description__icontains=search_value)
            try:
                price_search = Decimal(search_value)
            except Exception as e:
                pass
            else:
                query = query | Q(price=price_search)

            products = products.filter(
                query,
            )

    response = render(request, 'product_template.html', context={'products': products})

    return response


def product_by_id(request, product_id=None, *args, **kwargs):

    products = Product.objects.filter(id=product_id)
    if not products:
        raise Http404("Product does not exist")

    return render(request, 'product_template_single_product.html', context={'product': products.last()})
