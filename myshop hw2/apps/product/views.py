from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Product, ProductBrand
from apps.product.forms import SearchForm


class ProductsView(View):
    template_name = 'products.html'

    def get(self, request):
        form = SearchForm()

        products = Product.objects.all()

        context = {
            'products': products,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):

        products = Product.objects.all()
        form = SearchForm(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

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
        context = {
            'products': products,
            'form': form,
        }
        response = render(request, self.template_name, context=context)

        return response


def product_by_id(request, product_id=None, *args, **kwargs):
    print('in product_by_id')

    if not (products := Product.objects.filter(id=product_id)):
        raise Http404("Product does not exist")

    return render(request, 'product.html', context={'product': products.last()})


class BrandView(View):
    template_name = 'product_brands.html'

    def get(self, request):
        form = SearchForm()

        brands = ProductBrand.objects.all()

        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):

        brands = ProductBrand.objects.all()
        form = SearchForm(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            query = (Q(brand_name__icontains=search_value) | Q(brand_description__icontains=search_value)
                     | Q(brand_origin_country__icontains=search_value))
            brands = brands.filter(
                query,
            )
        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)

        return response


def brand_by_id(request, brand_id=None, *args, **kwargs):

    if not (brands := ProductBrand.objects.filter(id=brand_id)):
        raise Http404('Brand does not exist')

    return render(request, 'product_brand.html', context={'brand': brands.last()})
