from django import forms


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


class ProductToCartForm(forms.Form):
    pass
