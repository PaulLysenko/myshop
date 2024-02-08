from django import forms
from django.forms import ModelForm
from apps.product.product_schemas import ProductValidationSchema
from pydantic import ValidationError
from .models import Product


class SearchForm(forms.Form):
    search = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter exact name or exact price or partial description here ...',
                'class': 'form-control',
            },
        ),
    )


# class ProductToCartForm(forms.Form):
#     pass


class ProductImportForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        """"""
        value = self.cleaned_data.get('file')

        if value and value.name.split('.')[-1] != 'xlsx':
            raise forms.ValidationError('Not an .xlsx file')

        return value


class ProductValidationForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

    def validation_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 1:
            raise ValidationError("Error name length. Add at least 1 character.")
        else:
            self.cleaned_data['name'] = name.lower().strip()
        return name

    def validation_description(self):
        description = self.cleaned_data.get('description')

        if len(description) < 1:
            raise ValidationError("Error description length. Add at least 1 character.")
        return description

    def validation_price(self):
        price = self.cleaned_data.get('price')

        if price <= 0:
            raise ValidationError("Error price value. Price must be higher than zero.")
        return price


def validate_product_data(product_data):
    try:
        validated_product = ProductValidationSchema(**product_data)
        return None, validated_product.dict()
    except ValidationError:
        return ValidationError.errors(), None
