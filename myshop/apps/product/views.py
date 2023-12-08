from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from apps.product.models import Product
from apps.product.forms import SearchForm
from apps.product.models import Brand


class HomeView(TemplateView):
    template_name = 'base_layout.html'


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
    if not (products := Product.objects.filter(id=product_id)):
        raise Http404("Product does not exist")

    return render(request, 'product.html', context={'product': products.last()})


class BrandsView(View):
    template_name = 'brands.html'

    def get(self, request):
        form = SearchForm()
        brands = Brand.objects.all()

        context = {
            'brands': brands,
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = SearchForm(request.POST)
        brands = Brand.objects.all()

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            # query = Q(name__icontains=search_value)
            query = Q(name=search_value) | Q(description__icontains=search_value)
            brands = brands.filter(query)

        context = {
            'brands': brands,
            'form': form,
        }
        return render(request, self.template_name, context=context)


class BrandDetailView(View):
    template_name = 'brand.html'

    def get(self, request, brand_id=None, *args, **kwargs):
        brand = get_object_or_404(Brand, id=brand_id)

        context = {'brand': brand}
        return render(request, self.template_name, context=context)
