from hotelrebates.hotelloyalty import loyalty_rule


AMERICINN = 'AmericInn'
BAYMONT_INNS_AND_SUITES = 'Baymont Inns and Suites'
DAYS_INN = 'Days Inn'
DAZZLER = 'Dazzler'
ESPLENDOR = 'Esplendor'
HAWTHORN_SUITES_BY_WYNDHAM = 'Hawthorn Suites by Wyndham'
HOWARD_JOHNSON = 'Howard Johnson'
LA_QUINTA = 'La Quinta'
MICROTEL_INN_AND_SUITES_BY_WYNDHAM = 'Microtel Inn & Suites by Wyndham'
RAMADA = 'Ramada'
REGISTRY_COLLECTION = 'Registry Collection'
SUPER_8 = 'Super 8'
TRADEMARK = 'Trademark'
TRAVELODGE = 'Travelodge'
TRYP_BY_WYNDHAM = 'TRYP by Wyndham'
VIENNA_HOUSE_BY_WYNDHAM = 'Vienna House by Wyndham'
WINGATE_BY_WYNDHAM = 'Wingate by Wyndham'
WYNDHAM_ALLTRA = 'Wyndham Alltra'
PARTICIPATING_DESTINATIONS = 'Participating Destinations'
PARTICIPATING_CAESARS_REWARDS_PROPERTIES = 'Participating Caesars Rewards Properties'

DOLCE_HOTELS_AND_RESORTS = 'Dolce Hotels and Resorts'
WYNDHAM_GRAND = 'Wyndham Grand'
WYNDHAM_HOTELS_AND_RESORTS = 'Wyndham Hotels and Resorts'
VIVA_WYNDHAM_PROPERTIES = 'Viva Wyndham properties'
WYNDHAM_GARDEN_PROPERTIES = 'Wyndham Garden properties'

WATERWALK_EXTENDED_STAY_BY_WYNDHAM_FURNISHED = 'WaterWalk Extended Stay by Wyndham (Furnished Suites)'

WATERWALK_EXTENDED_STAY_BY_WYNDHAM_UNFURNISHED = 'WaterWalk Extended Stay by Wyndham (Unfurnished Suites)'
ECHO_SUITES_EXTENDED_STAY = 'ECHO Suites Extended Stay'


all_wyndham_brands = [
    AMERICINN, BAYMONT_INNS_AND_SUITES, DAYS_INN, DAZZLER, ESPLENDOR,
    HAWTHORN_SUITES_BY_WYNDHAM, HOWARD_JOHNSON, LA_QUINTA,
    MICROTEL_INN_AND_SUITES_BY_WYNDHAM, RAMADA, REGISTRY_COLLECTION, SUPER_8,
    TRADEMARK, TRAVELODGE, TRYP_BY_WYNDHAM, VIENNA_HOUSE_BY_WYNDHAM,
    WINGATE_BY_WYNDHAM, WYNDHAM_ALLTRA, PARTICIPATING_DESTINATIONS,
    PARTICIPATING_CAESARS_REWARDS_PROPERTIES, DOLCE_HOTELS_AND_RESORTS,
    WYNDHAM_GRAND, WYNDHAM_HOTELS_AND_RESORTS, VIVA_WYNDHAM_PROPERTIES,
    WYNDHAM_GARDEN_PROPERTIES, WATERWALK_EXTENDED_STAY_BY_WYNDHAM_FURNISHED, 
    WATERWALK_EXTENDED_STAY_BY_WYNDHAM_UNFURNISHED]

wyndham_loyalty_rules = [
    loyalty_rule.LoyaltyRule(id = 1, hotel_corporation='Wyndham', included_hotel_brands=[AMERICINN, BAYMONT_INNS_AND_SUITES,
        DAYS_INN, DAZZLER, ESPLENDOR, HOWARD_JOHNSON, LA_QUINTA,
        MICROTEL_INN_AND_SUITES_BY_WYNDHAM, RAMADA, SUPER_8,
        TRADEMARK, TRAVELODGE, TRYP_BY_WYNDHAM, VIENNA_HOUSE_BY_WYNDHAM,
        WYNDHAM_ALLTRA, PARTICIPATING_DESTINATIONS, PARTICIPATING_CAESARS_REWARDS_PROPERTIES],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 2, hotel_corporation='Wyndham', included_hotel_brands=[DOLCE_HOTELS_AND_RESORTS,
        WYNDHAM_GRAND, WYNDHAM_HOTELS_AND_RESORTS, VIVA_WYNDHAM_PROPERTIES,
        WYNDHAM_GARDEN_PROPERTIES],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=True)),
    loyalty_rule.LoyaltyRule(id = 3, hotel_corporation='Wyndham', included_hotel_brands=[WATERWALK_EXTENDED_STAY_BY_WYNDHAM_FURNISHED],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 4, hotel_corporation='Wyndham', included_hotel_brands=[WATERWALK_EXTENDED_STAY_BY_WYNDHAM_UNFURNISHED, ECHO_SUITES_EXTENDED_STAY],
        earn_action=loyalty_rule.EarnAction(earn_rate=0, earn_on_tax=False))
]