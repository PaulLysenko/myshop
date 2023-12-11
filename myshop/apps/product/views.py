from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Product, Brand
from apps.product.forms import SearchFormProduct, SearchFormBrand


class BrandsView(View):
    template_brands = 'brands.html'
    template_brand = 'brand.html'

    def get(self, request, brand_name=None, *args, **kwargs):

        brands = Brand.objects.all()
        form = SearchFormBrand(request.GET)

        if brand_name:
            try:
                brand = brands.filter(name__icontains=brand_name)
                if brand:
                    context = {
                        'brand': brand.last()
                    }
                    return render(request, self.template_brand, context=context)
                else:
                    raise Http404("Product does not exist")
            except Exception:
                raise Http404("Product does not exist")

        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_brands, context=context)
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
            response = render(request, self.template_brands, context=context)
            return response


class ProductsView(View):
    template_products = 'products.html'
    template_product = 'product.html'

    def get(self, request, product_id=None, *args, **kwargs):

        products = Product.objects.all()
        form = SearchFormProduct()

        if product_id:
            try:
                products = Product.objects.filter(id=product_id)
                if products:
                    context = {
                        'product': products.last()
                    }
                    return render(request, self.template_product, context=context)
                else:
                    raise Http404("Product does not exist")
            except Exception:
                raise Http404("Product does not exist")

        context = {
            'products': products,
            'form': form,
        }
        response = render(request, self.template_products, context=context)
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
        response = render(request, self.template_products, context=context)

        return response
