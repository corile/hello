from hotelrebates.hotelloyalty import loyalty_rule

# https://www.hilton.com/en/hilton-honors/member-benefits/
TRU = 'Tru & Home2 Suites'
LIVSMART = 'LivSmart Studios'
OTHER = 'Other Hilton Brands'

all_hilton_brands = [
    TRU, LIVSMART, OTHER
]

hilton_loyalty_rules = [
    loyalty_rule.LoyaltyRule(id = 1, hotel_corporation='Hilton', included_hotel_brands=[TRU],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 2, hotel_corporation='Hilton', included_hotel_brands=[LIVSMART],
        earn_action=loyalty_rule.EarnAction(earn_rate=3, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 3, hotel_corporation='Hilton', included_hotel_brands=[OTHER],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False))
]