#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`


# example card


#             <name>Opt</name>
#             <text>Scry 1.
# Draw a card.</text>
#             <prop>
#                 <format-oathbreaker>legal</format-oathbreaker>
#                 <format-modern>legal</format-modern>
#                 <format-pauper>legal</format-pauper>
#                 <maintype>Instant</maintype>
#                 <coloridentity>U</coloridentity>
#                 <format-explorer>legal</format-explorer>
#                 <format-vintage>legal</format-vintage>
#                 <format-pioneer>legal</format-pioneer>
#                 <format-gladiator>legal</format-gladiator>
#                 <format-brawl>legal</format-brawl>
#                 <cmc>1</cmc>
#                 <manacost>U</manacost>
#                 <type>Instant</type>
#                 <format-legacy>legal</format-legacy>
#                 <format-duel>legal</format-duel>
#                 <format-historic>legal</format-historic>
#                 <format-paupercommander>legal</format-paupercommander>
#                 <format-timeless>legal</format-timeless>
#                 <layout>normal</layout>
#                 <format-premodern>legal</format-premodern>
#                 <format-commander>legal</format-commander>
#                 <format-predh>legal</format-predh>
#                 <side>front</side>
#                 <colors>U</colors>
#             </prop>

import sys
import random
from card import Card
from cube_utils import displayStatsForCube, pruneCubeTo360, dumpCubeFile

from bs4 import BeautifulSoup
from collections import Counter

def main():
    """ 
    compiles the set of cards in ../cards.xml into a cube format

    cube format is just a file with the card names, with repeated card names for commons

    so for example

    Card One
    Fireball
    Lightning Bolt
    Omnipotence
    """

    try:
        # sys.argv[1] is expected to be -f for bash reasons
        filename = sys.argv[2]

        # open the input file as XML, input is assumed to be a cockatrice card file
        print("Loading file...")

        all_cards = allLegalCards(filename)

        displayStatsForCube(all_cards)

        all_cards = pruneCubeTo360(all_cards)

        dumpCubeFile(all_cards, "most_complex_cube.txt")

        word_count = 0
        for card in all_cards:
            word_count += len(card.text.split())
        print(f'total word count of cube: {word_count}')
        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 most_complex_cube.py -f filename")

# gets the entire list of legal cards
def allLegalCards(filename):

    all_available_cards = list()
    all_commons = list()
    all_uncommons = list()
    all_rares = list()
    all_mythics = list()

    with open(filename, "r") as f:
        soup_obj = BeautifulSoup(f, "xml")

        # grab the list of cards out of the input cockatrice xml file
        all_cards = soup_obj.findAll("card")

        for index in range(len(all_cards)):

            # grab the info and transform this into the Card instance format above
            cockatrice_card = all_cards[index]
            card = Card(cockatrice_card)

            # only append non-token rarities, and append twice if rarity is common
            if  card.rarity == 'token':
                continue

            # throw together all cards that pass the filter for each rarity, we'll prune them down later
            if passesFilter(card):
                all_available_cards.append(card)

                if card.rarity == 'common':
                    all_commons.append(card)
                if card.rarity == 'uncommon':
                    all_uncommons.append(card)
                if card.rarity == 'rare':
                    all_rares.append(card)
                if card.rarity == 'mythic':
                    all_mythics.append(card)

        print(f'cards legal in legacy: {len(all_available_cards)}/{len(all_cards)}')

    print(
        f'Lists calculated {len(all_commons)} {len(all_uncommons)} {len(all_rares)} {len(all_mythics)}')

    # sort the cards in place, we'll be able to pluck out cards by color later
    all_commons.sort()
    all_uncommons.sort()
    all_rares.sort()
    all_mythics.sort()

    return all_commons + all_uncommons + all_rares + all_mythics

# here's where a custom filter goes if we want one
def passesFilter(card):

    if 'Basic Land' in card.ctype:
        return False

    if not card.legal:
        return False

    if not card.side == 'front':
        return False

    return True        

if __name__ == "__main__":
    main()
