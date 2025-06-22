#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`

import sys

from bs4 import BeautifulSoup


def main():
    """ 
    compiles the set of cards in ../cards.xml into a singleton cube format file that can be imported into dr4ft.

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
        cube_list = set()

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

                        exclude = False

                        # these cards aren't supported in dr4ft (and aren't good/fun enough to work around)
                        if card_name in ["1996 World Champion", "Hazmat Suit (Used)"]:
                            exclude = True

                        for tag in cockatrice_card:
                            if tag.name == 'prop':
                                for type_tag in tag:
                                    if type_tag.name == 'maintype':
                                        if 'Scheme' in type_tag.string:
                                            print(
                                                f'filtering scheme ${card_name}')
                                            exclude = True
                                        if 'Phenomenon' in type_tag.string:
                                            print(
                                                f'filtering phenomenon ${card_name}')
                                            exclude = True
                                        if 'Vanguard' in type_tag.string:
                                            print(
                                                f'filtering vanguard ${card_name}')
                                            exclude = True
                                        if 'Hero' in type_tag.string:
                                            print(
                                                f'filtering hero ${card_name}')
                                            exclude = True
                                        if 'Plane' in type_tag.string:
                                            print(
                                                f'filtering plane ${card_name}')
                                            exclude = True

                                    if type_tag.name == 'type':
                                        if 'Basic Land' in type_tag.string:
                                            print(
                                                f'filtering basic land ${card_name}')
                                            exclude = True

                        if exclude:
                            continue

                        # only append non-token rarities, and append twice if rarity is common
                        for rarity_tag in cockatrice_card:
                            if rarity_tag.name == 'set':

                                # prune tokens
                                if rarity_tag['rarity'] == 'token':
                                    continue

                                cube_list.add(card_name)

        print(f'Writing {len(cube_list)} cards to cube file...')
        with open('example_cube.txt', 'w') as f:
            f.write('\n'.join(str(item) for item in cube_list))

        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 average_card_length.py -f filename")


if __name__ == "__main__":
    main()
