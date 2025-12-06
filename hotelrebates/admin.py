from django.contrib import admin

from hotelrebates.models import Bank, CashbackPortal, CreditCard, HotelCorporation, HotelEliteStatus, PortalOffer, TravelAgency, Currency

# Register your models here.
admin.site.register(HotelCorporation)
admin.site.register(HotelEliteStatus)
admin.site.register(Bank)
admin.site.register(Currency)
admin.site.register(CreditCard)
admin.site.register(TravelAgency)
admin.site.register(CashbackPortal)
admin.site.register(PortalOffer)