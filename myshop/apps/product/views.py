from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Product
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
    if not (products := Product.objects.filter(id=product_id)):
        raise Http404("Product does not exist")

    return render(request, 'product.html', context={'product': products.last()})
