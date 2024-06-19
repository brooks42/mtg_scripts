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
    def __init__(self, name, text, maintype, type, manacost, cmc, coloridentity, rarity, side):
        self.name = name
        self.text = text
        self.maintype = maintype
        self.type = type
        self.manacost = manacost
        self.cmc = cmc
        self.coloridentity = coloridentity
        self.rarity = rarity
        self.side = side

    # compile card from a card_node
    def __init__(self, card_node):
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
                        self.type = prop.string
                    if prop.name == 'manacost':
                        self.manacost = prop.string
                    if prop.name == 'cmc':
                        self.manacost = prop.string
                    if prop.name == 'coloridentity':
                        self.coloridentity = prop.string
                    if prop.name == 'side':
                        self.side = prop.string
            
            if node.name == 'set':
                self.rarity = node['rarity']
    

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

        dumpCubeFile(all_cards)

        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 rando_cubes.py -f filename")

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

            exclude = False

            # exclude some cards that don't work, as well as basic lands
            if card.name in ["1996 World Champion", "Hazmat Suit (Used)"]:
                exclude = True

            if 'Scheme' in card.maintype:
                exclude = True
            if 'Phenomenon' in card.maintype:
                exclude = True
            if 'Vanguard' in card.maintype:
                exclude = True
            if 'Hero' in card.maintype:
                exclude = True
            if 'Plane' in card.maintype:
                exclude = True

            if 'Basic Land' in card.type:
                exclude = True

            if exclude:
                continue

            # only append non-token rarities, and append twice if rarity is common
            if  card.rarity == 'token':
                continue

            if passesFilter(card):
                all_available_cards.append(card)
                if card.rarity == 'common':
                    all_commons.append(card)
                if card.rarity == 'uncommon':
                    all_uncommons.append(card)
                if card.rarity == 'rare':
                    all_rares.append(card)
                if card.rarity == 'mythic':
                    print(f'mythic found: {card.name}')
                    all_mythics.append(card)

    print(
        f'Lists calculated {len(all_commons)} {len(all_uncommons)} {len(all_rares)} {len(all_mythics)}')
    
    displayStatsForCube(all_available_cards)

    print("Filling out cube...")

    all_cards = fillOutCardsToCount(all_available_cards)

    displayStatsForCube(all_cards)
    
    return all_cards

# here's where a custom filter goes if we want one
def passesFilter(card):

    if card.text != None:
        word_count = len(card.text.split())

        if hasattr(card, 'side'):
            if word_count == 5 and card.side == 'front':
                return True
        else:
            if word_count == 5:
                return True

    return False

def fillOutCardsToCount(all_cards):

    modified_card_list = all_cards

    white, blue, black, red, green, colorless, multicolor = colorDistributionAmongCards(all_cards)

    # 360 is the size of a "normal" cube
    cards_to_pad = 360 - len(colorless) - len(multicolor)

    # if there's not a round number of cards to pad, add the first common colorless cards as dupes
    # TODO: this will break if there aren't enough colorless commons :)
    colorless_commons = cardsWithRarity(colorless, 'common')
    i = 0
    while cards_to_pad % 5 != 0:
        all_cards.append(colorless_commons[i])
        colorless.append(colorless_commons[i])
        cards_to_pad = 360 - len(colorless) - len(multicolor)
        i += 1

    # now get the number of cards of each color that we need to add in
    idealNumber = cards_to_pad / 5

    print(f'Ideal card count for each color is {idealNumber}')

    # pad out white cards
    rarity_passes = ['common', 'common', 'uncommon', 'rare', 'mythic']
    rarity_index = 0
    common_index = 0
    while len(white) < idealNumber:
        print('appending white card')
        current_rarity = rarity_passes[rarity_index]
        padding_cards = cardsWithRarity(white, current_rarity)

        if current_rarity == 'common':
            white.append(padding_cards[common_index])
            common_index += 1
        else:
            if len(padding_cards) > 0:
                white.append(padding_cards[0])
        
        rarity_index += 1
        if rarity_index > 4:
            rarity_index = 0

    # pad for blue cards
    rarity_index = 0
    common_index = 0
    while len(blue) < idealNumber:
        print('appending blue card')
        current_rarity = rarity_passes[rarity_index]
        padding_cards = cardsWithRarity(blue, current_rarity)

        if current_rarity == 'common':
            blue.append(padding_cards[common_index])
            common_index += 1
        else:
            if len(padding_cards) > 0:
                blue.append(padding_cards[0])
        
        rarity_index += 1
        if rarity_index > 4:
            rarity_index = 0

    # pad for black cards
    rarity_index = 0
    common_index = 0
    while len(black) < idealNumber:
        print('appending black card')
        current_rarity = rarity_passes[rarity_index]
        padding_cards = cardsWithRarity(black, current_rarity)

        if current_rarity == 'common':
            black.append(padding_cards[common_index])
            common_index += 1
        else:
            if len(padding_cards) > 0:
                black.append(padding_cards[0])
        
        rarity_index += 1
        if rarity_index > 4:
            rarity_index = 0
    
    # pad for red cards
    rarity_index = 0
    common_index = 0
    while len(red) < idealNumber:
        print('appending red card')
        current_rarity = rarity_passes[rarity_index]
        padding_cards = cardsWithRarity(red, current_rarity)

        if current_rarity == 'common':
            red.append(padding_cards[common_index])
            common_index += 1
        else:
            if len(padding_cards) > 0:
                red.append(padding_cards[0])
        
        rarity_index += 1
        if rarity_index > 4:
            rarity_index = 0

    # pad for green cards
    rarity_index = 0
    common_index = 0
    while len(green) < idealNumber:
        print('appending green card')
        current_rarity = rarity_passes[rarity_index]
        padding_cards = cardsWithRarity(green, current_rarity)

        if current_rarity == 'common':
            green.append(padding_cards[common_index])
            common_index += 1
        else:
            if len(padding_cards) > 0:
                green.append(padding_cards[0])
        
        rarity_index += 1
        if rarity_index > 4:
            rarity_index = 0

    modified_card_list = white + blue + black + red + green + colorless + multicolor

    return modified_card_list
        

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
        if hasattr(card, 'coloridentity'):
            if card.coloridentity == None:
                colorless.append(card)
            else:
                if card.coloridentity == 'W':
                    white.append(card)
                elif card.coloridentity == 'U':
                    blue.append(card)
                elif card.coloridentity == 'B':
                    black.append(card)
                elif card.coloridentity == 'R':
                    red.append(card)
                elif card.coloridentity == 'G':
                    green.append(card)
                else:
                    multicolor.append(card)
        else:
            colorless.append(card)

    return white, blue, black, red, green, colorless, multicolor

def printManaValuesOfCards(cards):
    print('1\t2\t3\t4\t5\t6\t7+')

# writes the passed list of cards to a file
def dumpCubeFile(cube_list):
    print(f'Writing {len(cube_list)} cards to cube file...')
    with open('weird_cube.txt', 'w') as f:
        f.write('\n'.join(str(item.name) for item in cube_list))

if __name__ == "__main__":
    main()
