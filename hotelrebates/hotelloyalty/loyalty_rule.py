class EarnAction:
    def __init__(self, earn_rate=0, earn_on_tax=False, max_nights_per_stay=9999):
        self.earn_rate = earn_rate
        self.earn_on_tax = earn_on_tax
        self.max_nights_per_stay = max_nights_per_stay

class LoyaltyRule:
    def __init__(
            self, 
            id,
            hotel_corporation, 
            included_hotel_brands = None, 
            exclude_hotel_brands = None,
            min_number_of_nights = 1, 
            max_number_of_nights = 99, 
            excluded_countries = None,
            earn_action = None):
        self.id = id
        self.hotel_corporation = hotel_corporation
        self.included_hotel_brands = included_hotel_brands
        self.exclude_hotel_brands = exclude_hotel_brands
        self.min_number_of_nights = min_number_of_nights
        self.max_number_of_nights = max_number_of_nights
        self.excluded_countries = excluded_countries
        self.earn_action = earn_action or EarnAction()

    def matches(self, hotel_corporation, hotel_brand, number_of_nights, country):
        if (hotel_corporation != self.hotel_corporation):
            return False
        if (self.included_hotel_brands is not None and
            hotel_brand not in self.included_hotel_brands):
            return False
        if (self.exclude_hotel_brands is not None and
            hotel_brand in self.exclude_hotel_brands):
            return False
        if (number_of_nights < self.min_number_of_nights or
            number_of_nights > self.max_number_of_nights):
            return False
        if (self.excluded_countries is not None and
            country in self.excluded_countries):
            return False
        return True

    def calculate_base_points(self, room_rate, taxes, number_of_nights) -> int:
        earnable_nights = min(number_of_nights, self.max_number_of_nights)
        if self.earn_action.earn_on_tax:
            return int(room_rate * self.earn_action.earn_rate * earnable_nights)
        return int((room_rate - taxes) * self.earn_action.earn_rate * earnable_nights)
    
