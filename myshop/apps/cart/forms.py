from django import forms

quantity_diapazone = [(i, str(i)) for i in range(1, 256)]


class CartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=quantity_diapazone, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
