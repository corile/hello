from django import forms

from hotelrebates.models import HotelCorporation
from hotelrebates.hotelloyalty import marriott_rules
import logging

class CalcForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Pop any custom kwargs before calling the parent constructor so
        # they are not passed to Django's Form __init__ (which would raise
        # TypeError on unexpected kwargs).
        brand_choices = kwargs.pop('brand_choices', None)
        super(CalcForm, self).__init__(*args, **kwargs)
        if brand_choices is not None:
            logging.debug(f"Initializing CalcForm with brand: {brand_choices}")
            self.fields['brand'].choices = brand_choices
        else:
            logging.debug("Initializing CalcForm without brand")

    corporation = forms.ModelChoiceField(label='Hotel Corporation', queryset=HotelCorporation.objects.all())
    # Start with no choices and render as a hidden input; Ajax will populate
    # the `brand` field choices and switch the widget to a select when needed.
    brand = forms.ChoiceField(label='Hotel Brand', choices=[])
    #brand = forms.ChoiceField(label='Hotel Brand', choices=[], widget=forms.HiddenInput(), required=False)
    nights = forms.IntegerField(label='Number of Nights', min_value=1)
    cash_price = forms.DecimalField(label='Cash Price (USD)', min_value=0)