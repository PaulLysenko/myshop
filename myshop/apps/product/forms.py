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


class ProductImportForm(forms.Form):

    file = forms.FileField()

    def clean_file(self):
        value = self.cleaned_data.get('file')

        if value and value.name.split('.')[-1] != 'xlsx':
            raise forms.ValidationError('Not an .xlsx file')

        return value
