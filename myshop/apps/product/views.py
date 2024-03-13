from decimal import Decimal

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

from apps.account.views import auth2required
from apps.product.constants import DEFAULT_PRODUCT_CACHE_TIME
from apps.product.models import Product, Brand
from apps.product.forms import SearchForm


class ProductsView(View):
    template_name = 'products.html'

    # @method_decorator(cache_page(10 * 60))
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('auth-login'))

        form = SearchForm()

        key = request.session.session_key
        if not (products := cache.get(key, [])):
            products = Product.objects.all()
            cache.set(
                key=key,
                value=products,
                timeout=DEFAULT_PRODUCT_CACHE_TIME,
            )
        products_paginator = Paginator(products, 2)
        page = request.GET.get('page')
        pagination_products = products_paginator.get_page(page)

        context = {
            # 'products': Product.cashed_objects.all(),
            'products': pagination_products,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    @method_decorator(login_required)
    @method_decorator(auth2required)
    def post(self, request):

        products = Product.objects.all().select_related(
            'brand',
        )
        form = SearchForm(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            query = Q(name=search_value) | \
                    Q(description__icontains=search_value) | \
                    Q(brand__name__icontains=search_value)
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


class ProductView(View):
    template = 'product.html'

    def get(self, request, product_id):
        if not (products := Product.objects.filter(id=product_id).select_related('brand')):
            raise Http404("Product does not exist")

        return render(request, self.template, context={'product': products.last(), 'product_id': product_id})


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
            query = Q(name=search_value) | Q(description__icontains=search_value)
            brands = brands.filter(query)

        context = {
            'brands': brands,
            'form': form,
        }
        return render(request, self.template_name, context=context)


class BrandDetailView(View):
    template_name = 'brand.html'

    def get(self, request, brand_id=None):
        brand = get_object_or_404(Brand, id=brand_id)

        context = {'brand': brand}
        return render(request, self.template_name, context=context)
