#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`

import sys
import random

from bs4 import BeautifulSoup


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
        cube_list = list()
        all_card_set = list()
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

                for name_tag in cockatrice_card:
                    if name_tag.name == 'name':
                        card_name = name_tag.string
                        # cmc = 0

                        exclude = False

                        if card_name in ["1996 World Champion", "Hazmat Suit (Used)"]:
                            exclude = True

                        for tag in cockatrice_card:
                            if tag.name == 'prop':
                                for type_tag in tag:
                                    if type_tag.name == 'maintype':
                                        if 'Scheme' in type_tag.string:
                                            exclude = True
                                        if 'Phenomenon' in type_tag.string:
                                            exclude = True
                                        if 'Vanguard' in type_tag.string:
                                            exclude = True
                                        if 'Hero' in type_tag.string:
                                            exclude = True
                                        if 'Plane' in type_tag.string:
                                            exclude = True

                                    if type_tag.name == 'type':
                                        if 'Basic Land' in type_tag.string:
                                            exclude = True

                        if exclude:
                            continue

                        # only append non-token rarities, and append twice if rarity is common
                        for rarity_tag in cockatrice_card:
                            if rarity_tag.name == 'set':

                                if rarity_tag['rarity'] == 'token':
                                    continue

                                # cube_list.add(card_name)

                                all_card_set.append(card_name)
                                if rarity_tag['rarity'] == 'common':
                                    all_commons.append(card_name)
                                if rarity_tag['rarity'] == 'uncommon':
                                    all_uncommons.append(card_name)
                                if rarity_tag['rarity'] == 'rare':
                                    all_rares.append(card_name)
                                if rarity_tag['rarity'] == 'mythic':
                                    all_mythics.append(card_name)

        print(
            f'Lists calculated {len(all_commons)} {len(all_uncommons)} {len(all_rares)} {len(all_mythics)}')

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
            cube_list.append(random.choice(all_card_set))

        print(f'Writing {len(cube_list)} cards to cube file...')
        with open('weird_cube.txt', 'w') as f:
            f.write('\n'.join(str(item) for item in cube_list))

        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 cube_compiler_script -f filename")


if __name__ == "__main__":
    main()
