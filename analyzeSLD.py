import json, sys
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from typing import List
from scipy.stats import skew

# Given a set of cards, calculate their average EDHRec rank
def avg_rank(cards):
    rank_list = []

    for card in cards:
        if 'edhrec_rank' in card:
            rank_list.append(card['edhrec_rank'])
    
    print(rank_list)
    rank_list = np.array(rank_list)
    averages = dict()
    averages['mean_rank'] = np.mean(rank_list)
    averages['median_rank'] = np.median(rank_list)
    averages['standard_deviation'] = np.std(rank_list)
    averages['skew'] = skew(rank_list)
    return averages

def z_scores(cards):
    
    for card in cards:

def calc_avgs(cards):
    norm_price_list = []
    foil_price_list = []

    for card in cards:
        if card['prices']['usd']:
            norm_price = Decimal(card['prices']['usd'])
            norm_price_list.append(norm_price)

        if card['prices']['usd_foil']:
            foil_price = Decimal(card['prices']['usd_foil'])
            foil_price_list.append(foil_price)
    
    norm_price_list = np.array(norm_price_list)
    foil_price_list = np.array(foil_price_list)
    averages = dict()
    averages['mean_norm'] = (np.mean(norm_price_list)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    averages['mean_foil']  = (np.mean(foil_price_list)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    averages['median_norm'] = (np.median(norm_price_list)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    averages['median_foil'] = (np.median(foil_price_list)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return averages

# Given a list of cards, generate a file sorting the cards from most to least expensive
def price_ranking(cards):
    # Build ranking for normal cards
    filtered_cards = [card for card in cards if card['prices'].get('usd')]
    sorted_cards = sorted(filtered_cards, key=lambda x: Decimal(x['prices']['usd']), reverse=True)
    with open("SLD_Norm_Prices.json", 'w') as out:
        json_cards = []
        for card in sorted_cards:
            json_cards.append({'name' : card['name'], 'price_usd' : card['prices']['usd']})
        json.dump(json_cards, out, indent=4)
    
    # Build ranking for foil cards
    filtered_cards = [card for card in cards if card['prices'].get('usd_foil')]
    sorted_cards = sorted(filtered_cards, key=lambda x: Decimal(x['prices']['usd_foil']), reverse=True)
    with open("SLD_Foil_Prices.json", 'w') as out:
        json_cards = []
        for card in sorted_cards:
            json_cards.append({'name' : card['name'], 'price_usd' : card['prices']['usd_foil']})
        json.dump(json_cards, out, indent=4)

if __name__ == "__main__":
    with open("SLD_Cards.json", 'r') as file:
        cards = json.load(file)
    
    averages = avg_rank(cards)
    averages.update(calc_avgs(cards))

    for key, value in averages.items():
        print(f"{key.replace('_', ' ').title()}: {value:.2f}")

    if "--prices" in sys.argv:
        print("Generating ranked price lists")
        price_ranking(cards)


        