from hotelrebates.hotelloyalty import loyalty_rule

STAYBRIDGE_SUITES = 'Staybridge Suites'
CANDLEWOOD_SUITES_AND_RESIDENCES = 'Candlewood Suites and Residences'
IHG_ARMY_HOTELS = 'IHG Army Hotels'
OTHER_IHG_BRANDS = 'Other IHG Brands'

all_ihg_brands = [
    STAYBRIDGE_SUITES, CANDLEWOOD_SUITES_AND_RESIDENCES, IHG_ARMY_HOTELS, OTHER_IHG_BRANDS
]

ihg_loyalty_rules = [
    loyalty_rule.LoyaltyRule(id = 1, hotel_corporation='IHG', included_hotel_brands=IHG_ARMY_HOTELS,
        earn_action=loyalty_rule.EarnAction(earn_rate=3, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 2, hotel_corporation='IHG', included_hotel_brands=[STAYBRIDGE_SUITES, CANDLEWOOD_SUITES_AND_RESIDENCES],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 3, hotel_corporation='IHG', included_hotel_brands=[OTHER_IHG_BRANDS],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False))
]