from django import forms


class SearchFormProduct(forms.Form):
    search = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter exact name or exact price or partial description here ...',
                'class': 'form-control',
            },
        ),
    )


class SearchFormBrand(forms.Form):
    search = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Brand\'s name or its country or describe it here ...',
                'class': 'form-control',
            },
        ),
    )
