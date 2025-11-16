from hotelrebates.hotelloyalty import loyalty_rule

# https://www.hyatt.com/help/terms/world-of-hyatt#IA
HYATT_STUDIOS_HOTEL = 'Hyatt Studios hotel'
OTHER = 'Other Hyatt Brands'

all_hyatt_brands = [
    HYATT_STUDIOS_HOTEL, OTHER
]

hyatt_loyalty_rules = [
    loyalty_rule.LoyaltyRule(id = 1, hotel_corporation='Hyatt', included_hotel_brands=[HYATT_STUDIOS_HOTEL],
        earn_action=loyalty_rule.EarnAction(earn_rate=2.5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 2, hotel_corporation='Hyatt', included_hotel_brands=[OTHER],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False))
]