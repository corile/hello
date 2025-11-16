from django.shortcuts import render
from django import forms
import logging

from hotelrebates.creditcards import credit_card_engine
from hotelrebates.currency import currency_engine
from hotelrebates.forms import CalcForm
from hotelrebates.hotelloyalty import hotel_loyalty_rule_engine, marriott_rules, choice_rules
from hotelrebates.ota import ota_engine

logger = logging.getLogger(__name__)

# Create your views here.
def calc (request):
    logger.info(f"calc view called with method={request.method}")
    form = CalcForm()
    if request.method == 'POST':
        corporation_id = request.POST.get('corporation')
        corporation_name = CalcForm().fields['corporation'].queryset.get(id=corporation_id).name
        brands = hotel_loyalty_rule_engine.get_brands_for_corporation(corporation_name)
        elite_levels = hotel_loyalty_rule_engine.get_elite_levels_for_corporation(corporation_name)
        form = CalcForm(request.POST, brand_choices=brands, elite_levels=elite_levels)
        logger.info(form.errors)
        if form.is_valid():
            logger.info("Form is valid, processing reservation")
            # Process the valid form data
            cash_price = form.cleaned_data['cash_price']
            corporation_name = form.cleaned_data['corporation'].name
            brand = form.cleaned_data['brand']
            nights = form.cleaned_data['nights']
            logger.debug(f"Cleaned data: corporation={corporation_name}, brand={brand}, nights={nights}, cash_price={cash_price}")

            elite_status_name = form.cleaned_data['elite_status']
            hotel_loyalty_points, hotel_rebates_value_in_cents = calculate_hotel_loyalty_points_and_value(
                request, 
                corporation_name, 
                brand, 
                elite_status_name, 
                cash_price, 
                nights)

            price_options = []
            all_credit_cards = credit_card_engine.get_all_credit_cards()
            all_travel_agencies = ota_engine.get_all_travel_agencies()

            for travel_agency in all_travel_agencies:
                for credit_card in all_credit_cards:
                    cc_rebates, cc_currency_id = credit_card_engine.calculate_credit_card_points(
                        credit_card_name=credit_card.card_name,
                        amount_spent_dollars=cash_price * nights,
                        hotel_corporation=corporation_name,
                        traveL_agency=travel_agency.name
                    )
                    cc_rebates_value_in_cents = currency_engine.calculate_points_value_in_cents(cc_currency_id, cc_rebates)
                    final_price = (float(cash_price) * nights) - (cc_rebates_value_in_cents / 100)
                    price_options.append({
                        'booking_channel': travel_agency.name,
                        'cash_price': f'${float(cash_price) * nights:.2f}',
                        'hotel_rebates_value': 'No hotel rebates for OTA bookings',
                        'hotel_rebates': '',
                        'credit_card_rebates_value': f'${cc_rebates_value_in_cents / 100:.2f}',
                        'credit_card_rebates': f'({cc_rebates} {credit_card.earn_currency.name} with {credit_card.card_name})',
                        'final_price': f'${final_price:.2f}',
                        'final_price_for_sorting': final_price
                    })

            for credit_card in all_credit_cards:
                cc_rebates, cc_currency_id = credit_card_engine.calculate_credit_card_points(
                    credit_card_name=credit_card.card_name,
                    amount_spent_dollars=cash_price * nights,
                    hotel_corporation=corporation_name,
                    traveL_agency=None
                )
                cc_rebates_value_in_cents = currency_engine.calculate_points_value_in_cents(cc_currency_id, cc_rebates)
                final_price = (float(cash_price) * nights) - (hotel_rebates_value_in_cents / 100) - (cc_rebates_value_in_cents / 100)
                price_options.append({
                    'booking_channel': f'Direct with {corporation_name}',
                    'cash_price': f'${float(cash_price) * nights:.2f}',
                    'hotel_rebates_value': f'${hotel_rebates_value_in_cents / 100:.2f}',
                    'hotel_rebates': f'({hotel_loyalty_points} {corporation_name} points)',
                    'credit_card_rebates_value': f'${cc_rebates_value_in_cents / 100:.2f}',
                    'credit_card_rebates': f'({cc_rebates} {credit_card.earn_currency.name} with {credit_card.card_name})',
                    'final_price': f'${final_price:.2f}',
                    'final_price_for_sorting': final_price
                })

            return render(
                request,
                'hotel_card.html',
                {
                    'form': form,
                    'hotel_name': f'{corporation_name} {brand}',
                    'price_options': sorted(price_options, key=lambda x: x['final_price_for_sorting'])
                })
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    return render(request, 'hotel_card.html', {'form': form})

def calculate_hotel_loyalty_points_and_value(request, corporation_name, brand, elite_status_name, cash_price, nights):
    hotel_loyalty_base_points, hotel_loyalty_currency_id = hotel_loyalty_rule_engine.calculate_base_points(
                    hotel_corporation=corporation_name,
                    hotel_brand=brand,
                    room_rate=float(cash_price),
                    taxes=0,
                    number_of_nights=nights
                )
    hotel_loyalty_bonus_points = hotel_loyalty_rule_engine.calculate_bonus_points(
                    hotel_corporation=corporation_name,
                    elite_status_name=elite_status_name,
                    base_points_earned=hotel_loyalty_base_points
                )
    hotel_loyalty_points = hotel_loyalty_base_points + hotel_loyalty_bonus_points
    logger.info(f"Calculated rebates={hotel_loyalty_points} for {corporation_name}/{brand}")
    hotel_rebates_value_in_cents = currency_engine.calculate_points_value_in_cents(hotel_loyalty_currency_id, hotel_loyalty_points)
    return hotel_loyalty_points, hotel_rebates_value_in_cents

def ajaxBrandField(request):
    logger.info("ajaxBrandField called")
    corporation_name = request.GET.get('corporation')
    logger.debug(f"corporation_name from GET: {corporation_name}")

    # Ensure the brand field exists and set choices returned by the rule engine.
    brands = hotel_loyalty_rule_engine.get_brands_for_corporation(corporation_name)
    logger.debug(f"Retrieved {len(brands)} brands for {corporation_name}")

    elite_levels = hotel_loyalty_rule_engine.get_elite_levels_for_corporation(corporation_name)
    logger.debug(f"Retrieved {len(elite_levels)} elite levels for {corporation_name}")

    # Render as a select so the returned fragment contains a visible <select>.
    form = CalcForm(brand_choices=brands, elite_levels=elite_levels)
    return render(request, 'brand_field.html', {'form': form})