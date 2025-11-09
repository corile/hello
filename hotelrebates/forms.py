from django import forms

from hotelrebates.models import Brand

class CalcForm(forms.Form):
    brand = forms.ModelChoiceField(label='Hotel Brand', queryset=Brand.objects.all())
    nights = forms.IntegerField(label='Number of Nights', min_value=1)
    cash_price = forms.DecimalField(label='Cash Price (USD)', min_value=0)