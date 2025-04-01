import requests, re, json
from typing import List, Dict
from enum import Enum, auto

URL = "https://api.scryfall.com/cards/search?q=set%3Asld+-type%3Abasic+-is%3Atoken&unique=cards&as=grid&order=name"
    
# Given a base URL, return a list of cards 
def gather_cards():
    collected_data = []
    url_data = read_page(URL)
    collected_data.extend(url_data['data'])
    
    while url_data['has_more']:
        url_data = read_page(url_data['next_page'])
        collected_data.extend(url_data['data'])

    return collected_data

# Given a URL, return the cards  
def read_page(url):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return(response.json())
    else:
        # Print an error message if the request was not successful
        print('Error:', response.status_code)
        return None

# Filter out tokens and lands 
def filter_non_cards(card_data):
    for i, card in enumerate(card_data):
        if card['layout'] == "token":
            del card_data[i]

# Test if any basics or tokens slipped through
def test_cards(cards: List[Dict]):
    isLegal = True
    for card in cards:
        if card['layout'] == "token":
            print(f"Card \"{card['name']}\" is a token")
            isLegal = False
        if "type_line" in card and re.search("Basic", card['type_line']):
            print(f"Card {card['name']} is basic")
            isLegal = False
    if isLegal:
        print("All cards legal")

if __name__ == "__main__":
    sld_cards = gather_cards()
    test_cards(sld_cards)
    with open("SLD_Cards.json", 'w') as out:
        out.write(json.dumps(sld_cards, indent = 4))
    