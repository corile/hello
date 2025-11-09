from django.contrib import admin

from hotelrebates.models import Bank, Brand, Currency

# Register your models here.
admin.site.register(Brand)
admin.site.register(Bank)
admin.site.register(Currency)