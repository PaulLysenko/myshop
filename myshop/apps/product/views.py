from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Product, ProductBrand
from apps.product.forms import SearchForm


class ProductsView(View):
    template_name = 'products.html'
    template_name2 = 'product.html'

    def get(self, request, product_id=None, *args, **kwargs):
        form = SearchForm()

        products = Product.objects.all()

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                context = {
                    'product': product,
                    'form': form
                }
                return render(request, self.template_name2, context=context)
            except:
                raise Http404('Brand does not exist')

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


class BrandView(View):
    template_name = 'product_brands.html'
    template_name2 = 'product_brand.html'

    def get(self, request, brand_id=None, *args, **kwargs):
        form = SearchForm()

        brands = ProductBrand.objects.all()

        if brand_id:
            try:
                brand = ProductBrand.objects.get(id=brand_id)
                context = {
                    'brand': brand,
                    'form': form
                }
                return render(request, self.template_name2, context=context)
            except:
                raise Http404('Brand does not exist')

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
            query = (Q(name__icontains=search_value) | Q(description__icontains=search_value)
                     | Q(country_of_origin__icontains=search_value))
            brands = brands.filter(
                query,
            )

        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)

        return response
