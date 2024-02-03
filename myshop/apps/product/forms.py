from django import forms
from django.forms import ModelForm
from pydantic import BaseModel, ValidationError, validator

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


# class ProductValidationForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'price', 'description']
#
#     def valid_name(self):
#         name = self.cleaned_data.get('name')
#         self.cleaned_data['name'] = name.strip()
#         self.cleaned_data['name'] = name.lower()
#         if len(name) < 1:
#             raise ValidationError("Name must be at least 1 characters long.")
#         return name
#
#     def valid_price(self):
#         price = self.cleaned_data.get('price')
#
#         if price <= 0:
#             raise ValidationError("Price must be > 0.")
#         return price
#
#     def valid_description(self):
#         description = self.cleaned_data.get('description')
#
#         if len(description) < 1:
#             raise ValidationError("Description must be at least 1 characters long.")
#         return description


class ProductSchema(BaseModel):
    name: str
    price: float
    description: str

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 1:
            raise ValueError("Name must be at least 1 character long.")
        return value

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        return value

    @validator("description")
    def validate_description(cls, value):
        if len(value) < 1:
            raise ValueError("Description must be at least 1 character long.")
        return value

def validate_product_data(product_data):
    try:
        validated_product = ProductSchema(**product_data)
        return None, validated_product.dict()
    except ValidationError as e:
        return e.errors(), None
