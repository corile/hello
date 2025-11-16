import logging
from hotelrebates.models import CreditCard

def get_all_credit_cards():
    return CreditCard.objects.all()

def get_credit_cards_for_bank(bank_name):
    return CreditCard.objects.filter(bank__name=bank_name)

def calculate_credit_card_points(credit_card_name, amount_spent_dollars, hotel_corporation=None, traveL_agency=None) -> tuple[int, int]:
    try:
        credit_card = CreditCard.objects.get(card_name=credit_card_name)
    except CreditCard.DoesNotExist:
        logging.error(f"Credit card '{credit_card_name}' does not exist.")
        return 0, 0

    if credit_card.earn_currency is None:
        logging.error(f"Currency not set for credit card: {credit_card_name}")
        return (0, 0)
    
    currency_id = credit_card.earn_currency.id

    # Points for travel portal bookings
    if traveL_agency and credit_card.travel_portal and credit_card.travel_portal.name == traveL_agency:
        if credit_card.travel_portal_points_per_dollar:
            points = int(amount_spent_dollars * credit_card.travel_portal_points_per_dollar)
            logging.info(f"Awarding {points} points for travel portal booking with card '{credit_card_name}'.")
            return points, currency_id
        
    # Points for hotel corporation bookings
    if hotel_corporation and credit_card.hotel_corporation and credit_card.hotel_corporation.name == hotel_corporation:
        total_points = 0
        if credit_card.hotel_corporation_points_per_stay:
            total_points += credit_card.hotel_corporation_points_per_stay
            logging.info(f"Awarding {credit_card.hotel_corporation_points_per_stay} points per stay for hotel corporation booking with card '{credit_card_name}'.")
        if credit_card.hotel_corporation_points_per_dollar:
            points = int(amount_spent_dollars * credit_card.hotel_corporation_points_per_dollar)
            logging.info(f"Awarding {points} points for hotel corporation booking with card '{credit_card_name}'.")
            return points + total_points, currency_id
        
    if credit_card.general_hotel_points_per_dollar:
        points = int(amount_spent_dollars * credit_card.general_hotel_points_per_dollar)
        logging.info(f"Awarding {points} points for general hotel booking with card '{credit_card_name}'.")
        return points, currency_id
    
    if traveL_agency and credit_card.ota_points_per_dollar:
        points = int(amount_spent_dollars * credit_card.ota_points_per_dollar)
        logging.info(f"Awarding {points} points for OTA booking with card '{credit_card_name}'.")
        return points, currency_id

    # Points for all other purchases
    if not credit_card.everywhere_points_per_dollar:
        logging.error(f"'everywhere_points_per_dollar' not set for credit card '{credit_card_name}'.")
        return 0, 0
    
    points = int(amount_spent_dollars * credit_card.everywhere_points_per_dollar)
    logging.info(f"Awarding {points} points for general spending with card '{credit_card_name}'.")
    return points, currency_id
