from django.shortcuts import render
from django import forms
import logging

from hotelrebates.creditcards import credit_card_engine
from hotelrebates.currency import currency_engine
from hotelrebates.forms import CalcForm
from hotelrebates.hotelloyalty import hotel_loyalty_rule_engine, marriott_rules, choice_rules
from hotelrebates.ota import ota_engine
from hotelrebates.portals import portal_engine

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
            elite_status_name = form.cleaned_data['elite_status']
            logger.debug(f"Cleaned data: corporation={corporation_name}, brand={brand}, nights={nights}, cash_price={cash_price}")

            price_options = []
            all_hotel_corporation_names = [_.name for _ in hotel_loyalty_rule_engine.get_all_hotel_corporations()]
            all_credit_cards = credit_card_engine.get_all_credit_cards()
            all_travel_agencies = ota_engine.get_all_travel_agencies()
            portals = portal_engine.get_all_portals()

            for travel_agency in all_travel_agencies:
                # Cannot book hotel through a different hotel corporation
                if (travel_agency.name in all_hotel_corporation_names and travel_agency.name != corporation_name):
                    continue
                hotel_loyalty_points, hotel_rebates_value_in_cents = calculate_hotel_loyalty_points_and_value(
                    corporation_name, 
                    brand, 
                    elite_status_name, 
                    travel_agency.name,
                    cash_price, 
                    nights)

                portal_rewards_for_ota = {}
                for portal in portals:
                    portal_rewards_for_ota[portal.name] = portal_engine.calculate_portal_rewards(portal.name, travel_agency.name, cash_price * nights)
                
                cc_rewards_for_ota = {}
                for credit_card in all_credit_cards:
                    cc_rewards_for_ota[credit_card.card_name] = credit_card_engine.calculate_credit_card_rewards(
                            credit_card_name=credit_card.card_name,
                            amount_spent_dollars=cash_price * nights,
                            hotel_corporation=corporation_name,
                            traveL_agency=travel_agency.name
                        )

                for portal in portals:
                    for credit_card in all_credit_cards:
                        cc_rebates, cc_rebates_value_in_cents = cc_rewards_for_ota[credit_card.card_name]
                        portal_rewards, portal_rewards_in_cents = portal_rewards_for_ota[portal.name]

                        final_price = (float(cash_price) * nights) - (hotel_rebates_value_in_cents / 100) - (cc_rebates_value_in_cents / 100) - (portal_rewards_in_cents / 100)
                        
                        price_options.append({
                            'booking_channel': travel_agency.name,
                            'cash_price': f'${float(cash_price) * nights:.2f}',
                            'hotel_rebates_value': f'${hotel_rebates_value_in_cents / 100:.2f}',
                            'hotel_rebates': f'({hotel_loyalty_points} {corporation_name} points)',
                            'credit_card_rebates_value': f'${cc_rebates_value_in_cents / 100:.2f}',
                            'credit_card_rebates': f'({cc_rebates} {credit_card.earn_currency.name} with {credit_card.card_name})',
                            'shopping_portal_rebates_value':  f'${portal_rewards_in_cents / 100:.2f}',
                            'shopping_portal_rebates': f'{portal_rewards} {portal.name} points',
                            'final_price': f'${final_price:.2f}',
                            'final_price_for_sorting': final_price
                        })

            # for credit_card in all_credit_cards:
            #     cc_rebates, cc_currency_id = credit_card_engine.calculate_credit_card_points(
            #             credit_card_name=credit_card.card_name,
            #             amount_spent_dollars=cash_price * nights,
            #             hotel_corporation=corporation_name,
            #             traveL_agency=None
            #         )
            #     cc_rebates_value_in_cents = currency_engine.calculate_points_value_in_cents(cc_currency_id, cc_rebates)
            #     portals = portal_engine.get_all_portals()
            #     for portal in portals:
            #         portal_rewards, portal_rewards_in_cents = portal_engine.calculate_portal_rewards(portal.name, corporation_name, cash_price * nights)
            #         final_price = (float(cash_price) * nights) - (hotel_rebates_value_in_cents / 100) - (cc_rebates_value_in_cents / 100) - (portal_rewards_in_cents / 100)
            #         price_options.append({
            #             'booking_channel': f'Direct with {corporation_name}',
            #             'cash_price': f'${float(cash_price) * nights:.2f}',
            #             'hotel_rebates_value': f'${hotel_rebates_value_in_cents / 100:.2f}',
            #             'hotel_rebates': f'({hotel_loyalty_points} {corporation_name} points)',
            #             'credit_card_rebates_value': f'${cc_rebates_value_in_cents / 100:.2f}',
            #             'credit_card_rebates': f'({cc_rebates} {credit_card.earn_currency.name} with {credit_card.card_name})',
            #             'shopping_portal_rebates_value':  f'${portal_rewards_in_cents / 100:.2f}',
            #             'shopping_portal_rebates': f'{portal_rewards} {portal.name} points',
            #             'final_price': f'${final_price:.2f}',
            #             'final_price_for_sorting': final_price
            #         })

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

def calculate_hotel_loyalty_points_and_value(corporation_name, brand, elite_status_name, travel_agency, cash_price, nights):
    # No hotel loyalty points for bookings not through the hotel chain.
    if (travel_agency != corporation_name):
        return 0,0
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