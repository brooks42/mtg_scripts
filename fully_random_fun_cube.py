#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`

import sys
from card import Card
from cube_utils import displayStatsForCube, pruneCubeTo360, dumpCubeFile, allLegalCards
import random

def main():

    try:
        # sys.argv[1] is expected to be -f for bash reasons
        filename = sys.argv[2]

        # open the input file as XML, input is assumed to be a cockatrice card file
        print("Loading file...")

        all_cards = allLegalCards(filename, passesFilter)

        random.shuffle(all_cards)

        displayStatsForCube(all_cards)

        all_cards = pruneCubeTo360(all_cards)

        dumpCubeFile(all_cards, "fully_random_fun_cube.txt")

        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 most_complex_cube.py -f filename")

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
