from django.db.models import Max
import logging
from hotelrebates.models import CashbackPortal, PortalOffer

def get_all_portals():
    return CashbackPortal.objects.all()

def calculate_portal_rewards(portal, travel_agency, total_spend_dollars):
    #max_value = PortalOffer.objects.aggregate(max_val=Max('last_seen'))['max_val']
    latest_offer_row = PortalOffer.objects.filter(
        portal__name=portal,
        travel_agency__name=travel_agency).order_by('-last_seen').first()
        #last_seen=max_value)
    if not latest_offer_row:
        logging.info(f'No offer found for {travel_agency} on {portal}')
        return 0,0
    
    cashback_rate = latest_offer_row.cashback_rate
    logging.info(f'Found offer for {travel_agency} on {portal} with rate {cashback_rate}%')
    return int(cashback_rate*total_spend_dollars), float(cashback_rate*total_spend_dollars)
