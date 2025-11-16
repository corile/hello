from django.contrib import admin

from hotelrebates.models import Bank, CreditCard, HotelCorporation, TravelAgency, Currency

# Register your models here.
admin.site.register(HotelCorporation)
admin.site.register(Bank)
admin.site.register(Currency)
admin.site.register(CreditCard)
admin.site.register(TravelAgency)