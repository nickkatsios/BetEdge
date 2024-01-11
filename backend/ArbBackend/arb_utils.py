from __future__ import absolute_import, unicode_literals

from .models import Arbitrage, ArbitrageOutcomes, Events, Markets, Odds
import os
from django.utils import timezone

# Define django settings at the top to be used accross all functions
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

def find_and_store_arbitrage_opportunities_football():
    """ Find and store all arbitrage opportunities."""

    events = Events.objects.all()
    markets = Markets.objects.all()

    for event in events:
        for market in markets:
            # Get the best odds for each option for the market
            best_odds = retrieve_best_event_market_odds(market_id=market.market_id, event_id=event.event_id)
            # Handle case where there are no odds for this market for this event
            if len(best_odds) == 0:
                continue
            # Begin if statements for each market type
            if market.market_id == 1: # Match Winner
                # No need for special handling for match winner
                # We call the arb calculation directly
                calculate_arbitrage_opportunities(best_odds , market.market_id, event.event_id) 
            elif market.market_id == 2: # Over/Under
                # Special handling for over/under
                calculate_arbitrage_over_under(best_odds, market.market_id, event.event_id)
                
def retrieve_best_event_market_odds(market_id, event_id):
    """ Retrieve all odds for a market for a single event from all bookmakers.
    
    We first retrieve all odds for the specified market for the specified event.
    And we order them by option_title and descending odds_value to get all values for an option with the highest one first.
    We then pick the first odd for each option_title (the one with the highest odds_value for that option_title).
    We now have a list of Odds objects for each option_title with the highest odds_value.
    For that option_title, we can now calculate arbitrage opportunities for these odds.

    If the best odds for an option title are located in the same bookmaker, then there is no problem
    since all other bookmakers will have lower odds for that option title. Since the single best bookmaker certainly has 
    an edge (ganiot), there is no arbitrage opportunity and we dont need to do anything.

    Returns:
        A list of Odds objects for each option_title with the highest odds_value.
    """
    event = Events.objects.get(event_id=event_id)
    # Get all odds for the specified market, for the specified event
    # ordered by option_title and descending odds_value
    odds_sorted = Odds.objects.filter(event_id=event_id, market_id=market_id).order_by('option_title' , '-odds_value')
    
    # Handle case where there are no odds for this market for this event
    if len(odds_sorted) == 0:
        print("No odds for event: " + str(event) + " market: " + str(market_id))
        return []
    
    # Pick the first odd for each option_title
    # (the one with the highest odds_value for that option_title)
    print("Event: " + str(event))
    best_odds = []
    current_option_title = odds_sorted[0].option_title
    best_odds.append(odds_sorted[0])
    for odd in odds_sorted:
        if odd.option_title != current_option_title:
            current_option_title = odd.option_title
            best_odds.append(odd)
    
    # We now have a list of Odds objects for each option_title with the highest odds_value
    # For that option_title, we can now calculate arbitrage opportunities for these odds.

    return best_odds

def calculate_arbitrage_opportunities(odds, market_id, event_id):
    """ Calculate arbitrage opportunities for a given set of odds from mutually exclusive outcomes.
    
    Arbitrage opportunities are calculated by summing the inverse of the odds for each outcome.
    If the sum is less than 1 then an arbitrage opportunity exists.

    Args:
        odds: A list of Odds of mutually exclusive outcomes.
    """
    arb_percentage = 0
    for odd in odds:
        arb_percentage += 1 / odd.odds_value
    if arb_percentage < 1.06 :
        print("Arb Found!")
        print("Arb Percentage: " + str(round(arb_percentage, 2)))
        for odd in odds:
            print("Odd: " + str(odd))
        # reduce decimal places to 3
        arb_percentage = round(arb_percentage, 3)
        handle_arbitrage(market_id, event_id, odds, arb_percentage)
        return
    
def handle_arbitrage(market_id, event_id, odds, arb_percentage):
    # check if arbitrage instance already exists
    if arbitrage_exists(market_id, event_id, arb_percentage):
        print("Arbitrage already exists in database. Skipping...")
        return
    else:
        print("Arbitrage does not exist in database. Saving...")
        save_arbitrage_opportunity(market_id, event_id, odds, arb_percentage)
            
def save_arbitrage_opportunity(market_id, event_id, odds, arb_percentage):
    arbitrage_instance = Arbitrage(
        event_id= Events.objects.get(event_id=event_id),
        market_id= Markets.objects.get(market_id=market_id),
        arbitrage_percentage=arb_percentage,
        timestamp=timezone.now()
    )
    arbitrage_instance.save()
    
    """ Save arbitrage outcomes for this opportunity to database."""
    for odd in odds:
        arbitrage_outcome_instance = ArbitrageOutcomes(
            arbitrage_id= Arbitrage.objects.get(arbitrage_id=arbitrage_instance.arbitrage_id),
            bookmaker_id= odd.bookmaker_id,
            outcome_title= odd.option_title,
            outcome_odds= odd.odds_value
        )
        arbitrage_outcome_instance.save()


def arbitrage_exists(market_id, event_id, arb_percentage):
    """ Check if arbitrage opportunity already exists in database. """
    arb_exists = Arbitrage.objects.filter(
        event_id= Events.objects.get(event_id=event_id),
        market_id= Markets.objects.get(market_id=market_id),
        arbitrage_percentage=arb_percentage
    ).exists()
    return arb_exists


def is_list_odd_length(list):
    """ Check if a list is of odd length. """
    return len(list) % 2 != 0

def match_mutually_exclusive_over_unders(odds):
    """ Match mutually exclusive over/under odds objects.
    
    Over/Under outcomes are mutually exclusive and we need to match them to calculate arbitrage opportunities.
    We do this by matching the over/under outcomes with the same option_title and odds_value.

    Args:
        odds: A list of the best odds for each option_title for the over under market for an event.

    Returns:
        A list of Odds objects of over unders with each mutually exclusive over/under in consecutive order.
        eg [over1, under1, over2, under2, ...]
    """
    matched_odds = {}

    for odd in odds:
        title_parts = odd.option_title.split()  # Split title into parts
        outcome_key = " ".join(title_parts[1:])  # Remove the "Over" or "Under" prefix
        if outcome_key not in matched_odds:
            matched_odds[outcome_key] = {"Over": None, "Under": None}
        if title_parts[0] == "Over":
            matched_odds[outcome_key]["Over"] = odd
        elif title_parts[0] == "Under":
            matched_odds[outcome_key]["Under"] = odd

    matched_odds_list = []
    for key, value in matched_odds.items():
        matched_odds_list.append(value["Over"])
        matched_odds_list.append(value["Under"])
    
    return matched_odds_list

def calculate_arbitrage_over_under(best_odds, market_id, event_id):
    """ Check for arbitrage opportunities in over/under markets.

    Over/Under outcomes are mutually exclusive and we need to match them to calculate arbitrage opportunities.
    We do this by matching the over/under outcomes with the same option_title and odds_value.
    We then check for arbitrage opportunities in each pair of over/under outcomes.
    If the list of over/under outcomes is odd length, we ignore the last odd outcome.

    Args:
        best_odds: A list of the best odds for each option_title for the over under market for an event.
    """
    matched_odds_list = match_mutually_exclusive_over_unders(best_odds)
    # Iterate through the matched over/unders in pairs
    for i in range(0, len(matched_odds_list), 2):
        # Check for arb in every pair
        # Check if list is odd length and if so, ignore the last odd
        if is_list_odd_length(matched_odds_list) and i == len(matched_odds_list) - 1:
            break
        else:
            # Else check the over/under pair for arb as usual
            over_under_pair = matched_odds_list[i:i+2]
            calculate_arbitrage_opportunities(over_under_pair, market_id, event_id)    
