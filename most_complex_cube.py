#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`

import sys
from card import Card
from cube_utils import displayStatsForCube, dumpCubeFile
from bs4 import BeautifulSoup

def main():

    try:
        # sys.argv[1] is expected to be -f for bash reasons
        filename = sys.argv[2]

        # open the input file as XML, input is assumed to be a cockatrice card file
        print("Loading file...")

        all_cards = allLegalCards(filename, passesFilter)

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

# gets the entire list of legal cards, including cards filtered by the passed filter
# filter takes a card and returns a boolean
# special version of this function that orders the cards by length when it returns them
def allLegalCards(filename, filter):

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
            if card.rarity == 'token':
                continue

            # throw together all cards that pass the filter for each rarity, we'll prune them down later
            if filter(card):
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
        
# prunes the cube to a color-balanced 360 cards
# special version of this function that sorts by card text length...
def pruneCubeTo360(all_cards: list[Card]):
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

        if color == 'colorless' and len(colorless_slots) < 50: # 50 is just a common max number for colorless cards
            colorless_slots.append(card)

        if color == 'multicolor' and len(multicolor_slots) < 60: # 60 is a common max number for multicolor cards
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
