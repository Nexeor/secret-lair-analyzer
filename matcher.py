import json
import re
import requests
from typing import List

REGEX_PATTERNS = {
    "card1" : r'^[\w\',\.\/\-]{9} [\w\',\.\/\-]{7} [\w\',\.\/\-]{4}$',
    "card2" : r'^[\w\',\.\/\-]{6} [\w\',\.\/\-]{7}$',
    "card3" : r'^[\w\',\.\/\-]{3} [\w\',\.\/\-]{2} [\w\',\.\/\-]{4}$',
    "card4" : r'^[\w\',\.\/\-]{11} [\w\',\.\/\-]{3}$',
    "card5" : r'^[\w\',\.\/\-]{11}$',
}

ALL_CARDNAMES_PATH = "cardNames.json"
OUTPUT_PATH = "matches"

# Takes a set of regex patterns and gathers the card data for cards with the matching name
class Matcher: 
    def __init__(self, patterns):
        self.patterns = patterns
        self.matches = [[] for _ in range(len(patterns))]
        self.URL = "https://api.scryfall.com/cards/named?exact="

    def match_all(self):
        """
        Match patterns against all card names and saves matches as instance value
        """
        self.match_file(ALL_CARDNAMES_PATH)
            
    def match_file(self, filename):
        """
        Match patterns against names in given file and saves matches as instance value
        """
        with open(filename) as file:
            self.match(json.load(file)['data'])

    def match(self, names) -> List[List]:
        """
        Match this matcher's patterns against the given set of names
        """
        for name in names:
            card_data = None
            for i, pattern in enumerate(self.patterns):
                if re.search(self.patterns[pattern], name):
                    if not card_data: # Only fetch the data once
                        card_data = self._get_card_data(name)
                    self.matches[i].append(card_data)

    def write_all_to_file(self):
        for i, pattern in enumerate(self.patterns):
            filepath = f"{OUTPUT_PATH}/matches_{pattern}.json"
            with open(filepath, 'w') as output:
                json.dump({"num_matches" : len(self.matches[i]), "matches" : self.matches[i]}, output, indent=4)

    def _get_card_data(self, cardname):
        newURL = f"{self.URL}{cardname}"
        cardFetch = requests.get(newURL)
        if cardFetch.status_code == 200:
            return cardFetch.json() 
        else:
            print(f"Can't find {cardname}")

if __name__ == "__main__":
    matcher = Matcher(REGEX_PATTERNS)
    matcher.match_all()
    print(matcher.matches)
    matcher.write_all_to_file()