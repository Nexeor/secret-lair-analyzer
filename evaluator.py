from typing import List 
import re, json, requests, sys, os

OUTPUT_PATH = "likely"

class Evaluator: 
    def __init__(self):
        self.validCards = []
    
    def evaluateCard(self, card : dict):
        """
        Given a json card, check if it meets minimum thresholds required
        
        Parameters:
        dict: json card
        
        Returns:
        boolean: true if card meets all critera, false otherwise
        """
        # print(card)
        isValid = True
        if 'edhrec_rank' not in card or card['edhrec_rank'] >= 4035:
            isValid = False
        elif card['rarity'] not in ["rare", "mythic"]:
            isValid = False
        return isValid
    
    def evaluateMatchFile(self, filepath):
        with open(filepath, 'r') as searchFile:
            cards = json.loads(searchFile.read())['matches']
            
            for card in cards:
                if self.evaluateCard(card):
                    self.validCards.append(card)
        self.validCards = sorted(self.validCards, key=lambda x: x['edhrec_rank'])    
    
    def write_to_file(self, filepath):
        with open(filepath, 'w') as output:            
            filtered_cards = [{k: d[k] for k in ["name", "edhrec_rank", "scryfall_uri"] if k in d} for d in self.validCards]
            json.dump({"num_matches" : len(filtered_cards), "likely_cards" : filtered_cards}, output, indent=4)

if __name__ == "__main__":
    evaluator = Evaluator()

    # Check a file of matches
    if "--file" in sys.argv:
        fileIndex = sys.argv.index('--file')
        if fileIndex + 1 < len(sys.argv):
            filepath = sys.argv[fileIndex + 1]
            print(f"Reading from: {filepath}")
            evaluator.evaluateMatchFile(filepath)

        if "--out" in sys.argv:
            fileIndex = sys.argv.index('--out')
            if fileIndex + 1 < len(sys.argv):
                filepath = f"{OUTPUT_PATH}/{sys.argv[fileIndex + 1]}"
                print(f"Writing to: {filepath}")
                evaluator.write_to_file(filepath)
    # Check all matches in the /matches directory
    if "--all" in sys.argv:
        dirPath = "matches"

    



