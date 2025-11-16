import logging

from hotelrebates.models import Currency

def calculate_points_value_in_cents(currency_id: int, points: int) -> int:
    currency = Currency.objects.get(id=currency_id)
    if currency.cpp is None:
        logging.error(f"Currency CPP not set for currency ID: {currency.id}")
        return 0
    return int(points * currency.cpp)