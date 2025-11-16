from hotelrebates.hotelloyalty import loyalty_rule

# https://www.choicehotels.com/choice-privileges/rules-regulations#earn
CAMBRIA = 'Cambria' 
CLARION = 'Clarion' 
CLARION_POINTE = 'Clarion Pointe'
COMFORT = 'Comfort'
ECONO_LODGE = 'Econo Lodge'
EVERHOME = 'Everhome'
MAINSTAY_SUITES = 'MainStay Suites'
QUALITY = 'Quality'
RODEWAY_INN = 'Rodeway Inn'
SLEEP_INN = 'Sleep Inn'
SUBURBAN_STUDIOS = 'Suburban Studios'
ASCEND_HOTEL_COLLECTION = 'Ascend Hotel Collection'
RADISSON_INDIVIDUALS = 'Radisson Individuals'
RADISSON_COLLECTION = 'Radisson Collection'
RADISSON_BLU = 'Radisson Blu'
RADISSON = 'Radisson'
RADISSON_RED = 'Radisson RED'
PARK_PLAZA = 'Park Plaza'
PARK_INN_BY_RADISSON = 'Park Inn by Radisson'
COUNTRY_INN_AND_SUITES_BY_RADISSON = 'Country Inn & Suites by Radisson'
WOODSPRING_SUITES = 'WoodSpring Suites'

extended_stay_brands = [MAINSTAY_SUITES, EVERHOME, SUBURBAN_STUDIOS]

all_choice_brands = [
    CAMBRIA,CLARION,CLARION_POINTE,COMFORT,ECONO_LODGE,EVERHOME,
    MAINSTAY_SUITES,QUALITY,RODEWAY_INN,SLEEP_INN,SUBURBAN_STUDIOS,
    ASCEND_HOTEL_COLLECTION,RADISSON_INDIVIDUALS,RADISSON_COLLECTION,RADISSON_BLU,RADISSON,
    RADISSON_RED,PARK_PLAZA,PARK_INN_BY_RADISSON,COUNTRY_INN_AND_SUITES_BY_RADISSON,WOODSPRING_SUITES]

choice_loyalty_rules = [
    loyalty_rule.LoyaltyRule(id = 1, hotel_corporation='Choice', included_hotel_brands=[WOODSPRING_SUITES],
        earn_action=loyalty_rule.EarnAction(earn_rate=0, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 2, hotel_corporation='Choice', included_hotel_brands=[CAMBRIA,CLARION,CLARION_POINTE,
        COMFORT, ECONO_LODGE,EVERHOME,MAINSTAY_SUITES,QUALITY,RODEWAY_INN,SLEEP_INN,SUBURBAN_STUDIOS,ASCEND_HOTEL_COLLECTION],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 3, hotel_corporation='Choice', included_hotel_brands=extended_stay_brands, 
                             max_number_of_nights=6,
                             earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(id = 4, hotel_corporation='Choice', included_hotel_brands=extended_stay_brands, 
                             min_number_of_nights=7,
                             earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False, max_nights_per_stay=30)),
    loyalty_rule.LoyaltyRule(id = 5, hotel_corporation='Choice', 
                             included_hotel_brands=all_choice_brands, exclude_hotel_brands=extended_stay_brands + [WOODSPRING_SUITES],
                             earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False))
]