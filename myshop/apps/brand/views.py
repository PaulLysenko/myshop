from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.brand.models import Brand
from apps.product.forms import SearchForm


class BrandView(View):
    template_name = 'brands.html'

    def get(self, request):
        form = SearchForm()

        brands = Brand.objects.all()

        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request):
        brands = Brand.objects.all()
        form = SearchForm(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            query = (Q(name_brand=search_value) | Q(description_brand__icontains=search_value)
                     | Q(country_brand=search_value))
            brands = brands.filter(
                query,
            )
        context = {
            'brands': brands,
            'form': form,
        }
        response = render(request, self.template_name, context=context)

        return response


class BrandByIdView(View):
    template_name = 'brand.html'

    def get(self, request, brand_id=None, *args, **kwargs):
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise Http404("Brand does not exist")

        return render(request, self.template_name, context={'brand': brand})
