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
    def __init__(self, name, text, maintype, type, manacost, cmc, coloridentity, rarity):
        self.name = name
        self.text = text
        self.maintype = maintype
        self.type = type
        self.manacost = manacost
        self.cmc = cmc
        self.coloridentity = coloridentity
        self.rarity = rarity

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

        all_cards, all_commons, all_uncommons, all_rares, all_mythics = allLegalCards(filename)

        cube_list = generateCubeFile(all_cards, all_commons, all_uncommons, all_rares, all_mythics)

        dumpCubeFile(cube_list)

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
            for rarity_tag in cockatrice_card:
                if rarity_tag.name == 'set':

                    if rarity_tag['rarity'] == 'token':
                        continue

                    if passesFilter(cockatrice_card):
                        all_available_cards.append(card)
                        if rarity_tag['rarity'] == 'common':
                            all_commons.append(card)
                        if rarity_tag['rarity'] == 'uncommon':
                            all_uncommons.append(card)
                        if rarity_tag['rarity'] == 'rare':
                            all_rares.append(card)
                        if rarity_tag['rarity'] == 'mythic':
                            all_mythics.append(card)

    print(
        f'Lists calculated {len(all_commons)} {len(all_uncommons)} {len(all_rares)} {len(all_mythics)}')
    
    return all_available_cards, all_commons, all_uncommons, all_rares, all_mythics

# here's where a custom filter goes if we want one
def passesFilter(card):

    for text_tag in card:
        if text_tag.name == 'text':
            if text_tag.string != None:

                word_count = len(text_tag.string.split())

                if word_count == 5:
                    print(f'checking {text_tag.string}: {word_count}')
                    return True

    return False

def displayStatsForCube(all_cards):
    print("Stats")
    print(f'Total cards: {all_cards}')

def colorDistributionAmongCards(all_cards):

    white = list()
    blue = list()
    black = list()
    red = list()
    green = list()

    for card in all_cards:
        for props_tag in card:
            if props_tag.name == 'prop':
                for color_identity_tag in card:
                    if color_identity_tag.name == 'coloridentity':
                        color_identity = color_identity_tag.string

                        if color_identity != None:
                            if 'w' in color_identity:
                                white.append(card)
                            if 'u' in color_identity:
                                blue.append(card)
                            if 'b' in color_identity:
                                black.append(card)
                            if 'r' in color_identity:
                                red.append(card)
                            if 'g' in color_identity:
                                green.append(card)

    return white, blue, black, red, green

def printManaValuesOfCards(cards):
    print('1\t2\t3\t4\t5\t6\t7+')

def generateCubeFile(all_cards, all_commons, all_uncommons, all_rares, all_mythics):

    cube_list = list()

    # generate cube list of all the proper cards
    # 60 commons
    for i in range(0, 60):
        cube_list.append(random.choice(all_commons))
    # 18 uncommons
    for i in range(0, 18):
        cube_list.append(random.choice(all_uncommons))
    # For rare/mythic logic, we could just lump them in the same bucket and pick 6, giving about 19.4% chance of getting a mythic.
    # Actual MTG distribution is 13.5% chance, so we'll go with that
    for i in range(0, 6):
        items = range(1, 201)
        check = random.choice(items)
        if check <= 27:
            cube_list.append(random.choice(all_mythics))
        else:
            cube_list.append(random.choice(all_rares))
    # 6 holos (any rarity)
    for i in range(0, 6):
        cube_list.append(random.choice(all_cards))

    return cube_list

# writes the passed list of cards to a file
def dumpCubeFile(cube_list):
    print(f'Writing {len(cube_list)} cards to cube file...')
    with open('weird_cube.txt', 'w') as f:
        f.write('\n'.join(str(item.name) for item in cube_list))

if __name__ == "__main__":
    main()
