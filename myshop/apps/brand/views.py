from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import Brand
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

        return render(request, self.template_name, context=context)

    def post(self, request):
        brands = Brand.objects.all()
        form = SearchForm(request.POST)

        form.is_valid()
        search_value = form.cleaned_data['search']

        if search_value:
            query = (Q(brand_name__icontains=search_value) | Q(brand_description__icontains=search_value)
                     | Q(brand_country__icontains=search_value))
            brands = brands.filter(
                query,
            )

        context = {
            'brands': brands,
            'form': form,
        }

        return render(request, self.template_name, context=context)


def brand_by_id(request, brand_id=None, *args, **kwargs):
    if not (brands := Brand.objects.filter(id=brand_id)):
        raise Http404('Brand does not exist')

    return render(request, 'brand.html', context={'brand': brands.last()})
