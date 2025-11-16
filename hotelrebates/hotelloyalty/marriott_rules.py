from . import loyalty_rule

EDITION = 'EDITION'
RITZ_CARLTON = 'The Ritz-Carlton'
LUXURY_COLLECTION = 'The Luxury Collection'
ST_REGIS = 'St. Regis' 
W_HOTELS = 'W Hotels'
JW_MARRIOTT = 'JW Marriott'
MARRIOTT_HOTELS = 'Marriott Hotels'
SHERATON = 'Sheraton'
MARRIOTT_VACATION_CLUB = 'Marriott Vacation Club'
DELTA_HOTELS_BY_MARRIOTT = 'Delta Hotels by Marriott'
WESTIN = 'Westin'
LE_MERIDIAN = 'Le Meridien'
RENAISSANCE_HOTELS = 'Renaissance Hotels'
AUTOGRAPH_COLLECTION = 'Autograph Collection'
TRIBUTE_PORTFOLIO = 'Tribute Portfolio'
DESIGN_HOTELS = 'Design Hotels'
GAYLORD_HOTELS = 'Gaylord Hotels'
MGM_COLLECTION_WITH_MARRIOTT_BONVOY = 'MGM Collection with Marriott Bonvoy™'
SONDER_BY_MARRIOTT_BONVOY_HOTELS = 'Sonder by Marriott Bonvoy, Hotels'
COURTYARD_BY_MARRIOTT = 'Courtyard by Marriott'
FOUR_POINTS_BY_SHERATON = 'Four Points by Sheraton'
SPRINGHILL_SUITES_BY_MARRIOTT = 'SpringHill Suites by Marriott'
FAIRFIELD_BY_MARRIOTT = 'Fairfield by Marriott'
AC_HOTELS_BY_MARRIOTT = 'AC Hotels by Marriott'
ALOFT = 'Aloft'
MOXY_HOTELS = 'Moxy Hotels'
OUTDOOR_COLLECTION_BY_MARRIOTT_BONVOY = 'Outdoor Collection by Marriott Bonvoy'
RESIDENCE_INN_BY_MARRIOTT = 'Residence Inn by Marriott'
TOWNEPLACE_SUITES_BY_MARRIOTT = 'TownePlace Suites by Marriott'
ELEMENT_BY_WESTIN = 'Element by Westin®'
HOMES_AND_VILLAS_BY_MARRIOTT_BONVOY = 'Homes & Villas by Marriott Bonvoy'
APARTMENTS_BY_MARRIOTT_BONVOY = 'Apartments by Marriott Bonvoy'
SONDER_BY_MARRIOTT_BONVOY_APARTMENTS = 'Sonder by Marriott Bonvoy, Apartments'
PROTEA_HOTELS_BY_MARRIOTT = 'Protea Hotels by Marriott'
CITY_EXPRESS_BY_MARRIOTT = 'City Express by Marriott'
FOUR_POINTS_FLEX_BY_SHERATON = 'Four Points Flex by Sheraton'
SERIES_BY_MARRIOTT = 'Series by Marriott'
STUDIO_RES = 'StudioRes'
MARRIOTT_EXECUTIVE_APARTMENTS = 'Marriott Executive Apartments'

all_marriott_brands = [
    EDITION,RITZ_CARLTON,LUXURY_COLLECTION,ST_REGIS,W_HOTELS,JW_MARRIOTT,
    MARRIOTT_HOTELS,SHERATON,MARRIOTT_VACATION_CLUB,DELTA_HOTELS_BY_MARRIOTT,
    WESTIN,LE_MERIDIAN,RENAISSANCE_HOTELS,AUTOGRAPH_COLLECTION,TRIBUTE_PORTFOLIO,
    DESIGN_HOTELS,GAYLORD_HOTELS,MGM_COLLECTION_WITH_MARRIOTT_BONVOY,
    SONDER_BY_MARRIOTT_BONVOY_HOTELS,COURTYARD_BY_MARRIOTT,FOUR_POINTS_BY_SHERATON,
    SPRINGHILL_SUITES_BY_MARRIOTT,FAIRFIELD_BY_MARRIOTT,AC_HOTELS_BY_MARRIOTT,ALOFT,MOXY_HOTELS,
    OUTDOOR_COLLECTION_BY_MARRIOTT_BONVOY,RESIDENCE_INN_BY_MARRIOTT,TOWNEPLACE_SUITES_BY_MARRIOTT,
    ELEMENT_BY_WESTIN,HOMES_AND_VILLAS_BY_MARRIOTT_BONVOY,APARTMENTS_BY_MARRIOTT_BONVOY,
    SONDER_BY_MARRIOTT_BONVOY_APARTMENTS,PROTEA_HOTELS_BY_MARRIOTT,CITY_EXPRESS_BY_MARRIOTT,
    FOUR_POINTS_FLEX_BY_SHERATON,SERIES_BY_MARRIOTT,STUDIO_RES,MARRIOTT_EXECUTIVE_APARTMENTS]

marriott_loyalty_rules = [
    loyalty_rule.LoyaltyRule(
        id=1,
        hotel_corporation='Marriott', 
        included_hotel_brands=[
            EDITION,RITZ_CARLTON,LUXURY_COLLECTION,ST_REGIS,W_HOTELS,JW_MARRIOTT,
            MARRIOTT_HOTELS,SHERATON,MARRIOTT_VACATION_CLUB,DELTA_HOTELS_BY_MARRIOTT,
            WESTIN,LE_MERIDIAN,RENAISSANCE_HOTELS,AUTOGRAPH_COLLECTION,TRIBUTE_PORTFOLIO,
            DESIGN_HOTELS,GAYLORD_HOTELS,MGM_COLLECTION_WITH_MARRIOTT_BONVOY,
            SONDER_BY_MARRIOTT_BONVOY_HOTELS,COURTYARD_BY_MARRIOTT,FOUR_POINTS_BY_SHERATON,
            SPRINGHILL_SUITES_BY_MARRIOTT,FAIRFIELD_BY_MARRIOTT,AC_HOTELS_BY_MARRIOTT,ALOFT,MOXY_HOTELS,
            OUTDOOR_COLLECTION_BY_MARRIOTT_BONVOY],
        earn_action=loyalty_rule.EarnAction(earn_rate=10, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(
        id=2,
        hotel_corporation='Marriott',
        included_hotel_brands=[
            RESIDENCE_INN_BY_MARRIOTT,TOWNEPLACE_SUITES_BY_MARRIOTT,ELEMENT_BY_WESTIN,
            HOMES_AND_VILLAS_BY_MARRIOTT_BONVOY,APARTMENTS_BY_MARRIOTT_BONVOY,
            SONDER_BY_MARRIOTT_BONVOY_APARTMENTS],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(
        id=3,
        hotel_corporation='Marriott',
        included_hotel_brands=[
            PROTEA_HOTELS_BY_MARRIOTT,CITY_EXPRESS_BY_MARRIOTT,FOUR_POINTS_FLEX_BY_SHERATON,
            SERIES_BY_MARRIOTT],
        earn_action=loyalty_rule.EarnAction(earn_rate=5, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(
        id=4,
        hotel_corporation='Marriott',
        included_hotel_brands=[
            STUDIO_RES],
        earn_action=loyalty_rule.EarnAction(earn_rate=4, earn_on_tax=False)),
    loyalty_rule.LoyaltyRule(
        id=5,
        hotel_corporation='Marriott',
        included_hotel_brands=[
            MARRIOTT_EXECUTIVE_APARTMENTS],
        earn_action=loyalty_rule.EarnAction(earn_rate=2.5, earn_on_tax=False)),
]