from hotelrebates.hotelloyalty import hilton_rules, hyatt_rules, ihg_rules, marriott_rules, choice_rules, wyndham_rules
from hotelrebates.models import Currency, HotelCorporation
import logging

loyalty_rules_map = {
    "Marriott": marriott_rules.marriott_loyalty_rules,
    "Choice": choice_rules.choice_loyalty_rules,
    "Hilton": hilton_rules.hilton_loyalty_rules,
    "Hyatt": hyatt_rules.hyatt_loyalty_rules,
    "IHG": ihg_rules.ihg_loyalty_rules,
    "Wyndham": wyndham_rules.wyndham_loyalty_rules
}

hotel_brands_map = {
    "Marriott": marriott_rules.all_marriott_brands,
    "Choice": choice_rules.all_choice_brands,
    "Hilton": hilton_rules.all_hilton_brands,
    "Hyatt": hyatt_rules.all_hyatt_brands,
    "IHG": ihg_rules.all_ihg_brands,
    "Wyndham": wyndham_rules.all_wyndham_brands
}

def calculate_base_points(hotel_corporation, hotel_brand, room_rate, taxes, number_of_nights) -> tuple[int, int]:
    if hotel_corporation not in loyalty_rules_map:
        logging.warning(f"No loyalty rules found for hotel corporation: {hotel_corporation}")
        return (0, 0)
    hotel_corporation_obj = HotelCorporation.objects.get(name=hotel_corporation)
    if hotel_corporation_obj.currency is None:
        logging.error(f"Currency not set for hotel corporation: {hotel_corporation}")
        return (0, 0)
    for rule in loyalty_rules_map[hotel_corporation]:
        if rule.matches(hotel_corporation, hotel_brand, number_of_nights, country=None):
            logging.info(f"Applying loyalty rule ID {rule.id} for hotel corporation: {hotel_corporation}, brand: {hotel_brand}")
            return rule.calculate_base_points(room_rate, taxes, number_of_nights), hotel_corporation_obj.currency.id
    return (0, 0)

def get_brands_for_corporation(hotel_corporation):
    if hotel_corporation in hotel_brands_map:
        return [(brand, brand) for brand in hotel_brands_map[hotel_corporation]]
    return []