from django.shortcuts import render


def product(request, *args, **kwargs):

    print(f'inside product')

    return render(request, 'product_template.html')
