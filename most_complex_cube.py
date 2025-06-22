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

from bs4 import BeautifulSoup
from collections import Counter

class Card:
    def __init__(self, name, text, maintype, ctype, manacost, cmc, color_identity, rarity, side, legal):
        self.name = name
        self.text = text
        self.maintype = maintype
        self.type = ctype
        self.manacost = manacost
        self.cmc = cmc
        self.color_identity = color_identity
        self.rarity = rarity
        self.side = side
        self.legal = legal

    # compile card from a card_node
    def __init__(self, card_node):
        self.legal = False # this gets set to true if the card is legal in legacy
        self.color_identity = None

        for node in card_node:
            if node.name == 'name':
                self.name = node.string

            if node.name == 'text':
                self.text = node.string

            if node.name == 'prop':
                for prop in node:
                    if prop.name == 'maintype':
                        self.maintype = prop.string
                    if prop.name == 'type':
                        self.ctype = prop.string
                    if prop.name == 'manacost':
                        self.manacost = prop.string
                    if prop.name == 'cmc':
                        self.manacost = prop.string
                    if prop.name == 'coloridentity':
                        self.color_identity = prop.string
                    if prop.name == 'side':
                        self.side = prop.string
                    if prop.name == 'format-vintage':
                        self.legal = prop.string == 'legal' or prop.string == 'limited'
            
            if node.name == 'set':
                self.rarity = node['rarity']

    # overwrite sort to sort by text length
    def __lt__(self, other):
        if self.text != None and other.text != None:
            return len(self.text.split()) < len(other.text.split())

        # cards with words sort higher than cards with no words
        if self.text != None and other.text == None:
            return False
        
        return True 

    def colorIdentityStr(self):
        # print(f'checking color identity for {self.color_identity}')
        if self.color_identity == None or self.color_identity == '':
            return 'colorless'
        if len(self.color_identity) > 1:
            return 'multicolor'
        return self.color_identity
    

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

        dumpCubeFile(all_cards)

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

# prints the stats of the cube
def displayStatsForCube(all_cards):
    print("Stats")
    print(f'Total cards: {len(all_cards)}')
    
    white, blue, black, red, green, colorless, multicolor = colorDistributionAmongCards(all_cards)
    print(f'{len(white)} White')
    print(f'{len(blue)} Blue')
    print(f'{len(black)} Black')
    print(f'{len(red)} Red')
    print(f'{len(green)} Green')
    print(f'{len(colorless)} Colorless')
    print(f'{len(multicolor)} Multicolor')

    print(f"White rarities: {rarityCount(white, 'common')}/{rarityCount(white, 'uncommon')}/{rarityCount(white, 'rare')}/{rarityCount(white, 'mythic')}")
    print(f"Blue rarities: {rarityCount(blue, 'common')}/{rarityCount(blue, 'uncommon')}/{rarityCount(blue, 'rare')}/{rarityCount(blue, 'mythic')}")
    print(f"Black rarities: {rarityCount(black, 'common')}/{rarityCount(black, 'uncommon')}/{rarityCount(black, 'rare')}/{rarityCount(black, 'mythic')}")
    print(f"Red rarities: {rarityCount(red, 'common')}/{rarityCount(red, 'uncommon')}/{rarityCount(red, 'rare')}/{rarityCount(red, 'mythic')}")
    print(f"Green rarities: {rarityCount(green, 'common')}/{rarityCount(green, 'uncommon')}/{rarityCount(green, 'rare')}/{rarityCount(green, 'mythic')}")
    print(f"Colorless rarities: {rarityCount(colorless, 'common')}/{rarityCount(colorless, 'uncommon')}/{rarityCount(colorless, 'rare')}/{rarityCount(colorless, 'mythic')}")
    print(f"Multicolor rarities: {rarityCount(multicolor, 'common')}/{rarityCount(multicolor, 'uncommon')}/{rarityCount(multicolor, 'rare')}/{rarityCount(multicolor, 'mythic')}")
    
def cardsWithRarity(cards, rarity):
    check = list()

    for card in cards:
        if card.rarity == rarity:
            check.append(card)

    return check

# returns the number of cards in the passed list with the given rarity
def rarityCount(cards, rarity):
    return len(cardsWithRarity(cards, rarity))

# gets the color distribution across all the passed cards
def colorDistributionAmongCards(all_cards):

    white = list()
    blue = list()
    black = list()
    red = list()
    green = list()
    colorless = list()
    multicolor = list()

    for card in all_cards:
        color = card.colorIdentityStr()
        if color == 'colorless':
            colorless.append(card)
        if color == 'W':
            white.append(card)
        elif color == 'U':
            blue.append(card)
        elif color == 'B':
            black.append(card)
        elif color == 'R':
            red.append(card)
        elif color == 'G':
            green.append(card)
        else:
            multicolor.append(card)

    return white, blue, black, red, green, colorless, multicolor

# print the mana values of cards, not used yet
def printManaValuesOfCards(cards):
    print('1\t2\t3\t4\t5\t6\t7+')

# prunes the cube to a color-balanced 360 cards
# 
def pruneCubeTo360(all_cards):
    white_slots = list()
    blue_slots = list()
    black_slots = list()
    red_slots = list()
    green_slots = list()
    colorless_slots = list()
    multicolor_slots = list()

    all_cards.sort()
    all_cards.reverse()
    for card in all_cards:
        color = card.colorIdentityStr()

        if color == 'colorless' and len(colorless_slots) < 50:
            colorless_slots.append(card)

        if color == 'multicolor' and len(multicolor_slots) < 60:
            multicolor_slots.append(card)
            
        if color == 'W' and len(white_slots) < 50:
            white_slots.append(card)

        if color == 'U' and len(blue_slots) < 50:
            blue_slots.append(card)

        if color == 'B' and len(black_slots) < 50:
            black_slots.append(card)

        if color == 'R' and len(red_slots) < 50:
            red_slots.append(card)

        if color == 'G' and len(green_slots) < 50:
            green_slots.append(card)

        # check to return list, otherwise keep going...
        if len(white_slots) == 50 and len(blue_slots) == 50 and len(black_slots) == 50 and len(red_slots) == 50 and len(green_slots) == 50 and len(colorless_slots) == 50 and len(multicolor_slots) == 60:
            break

    all_done = white_slots + blue_slots + black_slots + red_slots + green_slots + colorless_slots + multicolor_slots
    print(f'Compiled cube list from {len(all_cards)} to {len(all_done)}')
    return all_done

# writes the passed list of cards to a file
def dumpCubeFile(cube_list):
    print(f'Writing {len(cube_list)} cards to cube file...')
    with open('weird_cube.txt', 'w') as f:
        f.write('\n'.join(str(item.name) for item in cube_list))

if __name__ == "__main__":
    main()
