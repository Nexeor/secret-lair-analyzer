from typing import List 
import re, json, requests, sys, os

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

    # Given a file of matches, check them for the criteria
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
    

    



