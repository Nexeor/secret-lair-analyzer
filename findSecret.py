from typing import List 
import re, json, requests, sys, os

REGEX_PATTERNS = {
    "card1" : r'^[\w\',\.\/\-]{9} [\w\',\.\/\-]{7} [\w\',\.\/\-]{4}$',
    "card2" : r'^[\w\',\.\/\-]{6} [\w\',\.\/\-]{7}$',
    "card3" : r'^[\w\',\.\/\-]{3} [\w\',\.\/\-]{2} [\w\',\.\/\-]{4}$',
    "card4" : r'^[\w\',\.\/\-]{11} [\w\',\.\/\-]{3}$',
    "card5" : r'^[\w\',\.\/\-]{11}$',
}

URL = "https://api.scryfall.com/cards/named?exact="

# Run the set of regex patterns on all cardnames, one by one
# Create a file of matches for each regex
def gather_matches():
    for card_pattern in REGEX_PATTERNS:
        filepath = f"matches/pattern_matches_{card_pattern}.json"
        with open(filepath, 'w') as output:
            matches = find_matches(REGEX_PATTERNS[card_pattern])
            json.dump(matches, output, indent=4)

# Given a regex string, return all cards matching that regex
def find_matches(regex):
    matches = []
    with open("cardNames.json") as file:
        set = json.load(file)
        
        for cardname in set['data']:
            if re.search(regex, cardname):
                matches.append(get_card_data(cardname))
            
    return matches

# Given a card name, query Scryfall and fetch its data
def get_card_data(cardname):
    newURL = f"{URL}{cardname}"
    cardFetch = requests.get(newURL)
    if cardFetch.status_code == 200:
        return cardFetch.json() 
    else:
        print(f"Can't find {cardname}")

# Given a card dict, check if it meets minimum thresholds required
def checkCard(card):
    isValid = True
    if not card['edh_rank'] or card['edhrec_rank'] <= 4035:
        isValid = False
    elif card['rarity'] not in ["rare", "mythic"]:
        isValid = False
    return isValid

def checkSearchFile(filepath):
    with open(filepath, 'r') as searchFile:
        cards = json.loads(searchFile)
        
        validCards = []
        for card in cards:
            if checkCard(card):
                validCards.append(card)
    
    return validCards

if __name__ == "__main__":
    validCards = checkSearchFile()

    if "--file" in sys.argv:
        fileIndex = sys.argv.index('--file')
        if fileIndex + 1 < len(sys.argv):
            filepath = sys.argv[fileIndex + 1]
            print(f"filepath: {filepath}")
            checkSearchFile(filepath)
    if "--all" in sys.argv:
        dirPath = "matches"
    if "--match" in sys.argv:
        gather_matches()
    

    



