from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Product, Brand
from apps.product.forms import SearchFormProduct, SearchFormBrand


class BrandsView(View):
    template_name = 'brands.html'

    def get(self, request):

        brands = Brand.objects.all()
        form = SearchFormBrand(request.GET)

        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):

        brands = Brand.objects.all()
        form = SearchFormBrand(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            query = Q(name__icontains=search_value) | Q(description__icontains=search_value) | Q(country__icontains=search_value)
            brands = brands.filter(query)
            context = {
                'brands': brands,
                'form': form,
            }
            response = render(request, self.template_name, context=context)
            return response

    @staticmethod
    def brand_by_name(request, brand_name=None, *args, **kwargs):
        if not (brands := Brand.objects.filter(name=brand_name)):
            raise Http404("Product does not exist")

        return render(request, 'brand.html', context={'brand': brands.last()})



class ProductsView(View):
    template_name = 'products.html'

    def get(self, request):

        products = Product.objects.all()
        form = SearchFormProduct()

        context = {
            'products': products,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):

        products = Product.objects.all()
        form = SearchFormProduct(request.POST)

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

    @staticmethod
    def product_by_id(request, product_id=None, *args, **kwargs):

        if not (products := Product.objects.filter(id=product_id)):
            raise Http404("Product does not exist")

        return render(request, 'product.html', context={'product': products.last()})
