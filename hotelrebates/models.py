from django.db import models

# Create your models here.
class HotelCorporation(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True)
    terms_and_conditions = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class HotelEliteStatus(models.Model):
    corporation = models.ForeignKey(HotelCorporation, on_delete=models.CASCADE)
    status_name = models.CharField(max_length=100)
    points_earning_bonus_percent = models.IntegerField()

    def __str__(self):
        return f"{self.status_name} ({self.corporation.name})"

class Bank(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    name = models.CharField(max_length=100)
    cpp = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name
    
class TravelAgency(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CreditCard(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=100)
    earn_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    # Earn rate at all general hotels
    general_hotel_points_per_dollar = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)

    # Earn bonus points for specific hotel corporation
    hotel_corporation = models.ForeignKey(HotelCorporation, on_delete=models.CASCADE, null=True, blank=True)
    hotel_corporation_points_per_dollar = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    hotel_corporation_points_per_stay = models.IntegerField(null=True, blank=True)

    # Earn bonus points for booking through any online travel agency
    ota_points_per_dollar = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    
    # Earn bonus points for bookings made via specific travel portal
    travel_portal_points_per_dollar = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    travel_portal = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, null=True, blank=True)

    # Earn bonus points on all other purchases
    everywhere_points_per_dollar = models.DecimalField(max_digits=5, decimal_places=3, null=False, blank=False)
    def __str__(self):
        return f"{self.card_name} ({self.bank.name})"
    
class CashbackPortal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class PortalOffer(models.Model):
    portal = models.ForeignKey(CashbackPortal, on_delete=models.CASCADE)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE)
    cashback_rate = models.DecimalField(max_digits=5, decimal_places=2)
    terms_and_conditions = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.last_seen}] {self.portal.name} - {self.travel_agency.name} Offer"