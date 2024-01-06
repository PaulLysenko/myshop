from django import forms


quantity_choices = [(i, str(i)) for i in range(1, 256)]  # це так задумано, фіча


class CartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=quantity_choices,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
