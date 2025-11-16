import logging
from hotelrebates.models import TravelAgency

def get_all_travel_agencies():
    return TravelAgency.objects.all()