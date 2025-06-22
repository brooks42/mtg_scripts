#!/usr/bin/env python

# xml parsing help from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/?ref=lbp
# to run you need to do
# `pip3 install beautifulsoup4`
# `pip3 install lxml`
# `pip3 install xmltodict`

import sys
import xmltodict


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

        total_cards = 0
        combined_length_of_all_card_texts = 0

        with open(filename, "r") as file:
            # soup_obj = BeautifulSoup(f, "xml")

            # grab the list of cards out of the input cockatrice xml file
            # all_cards = soup_obj.findAll("card")

            xml_content = file.read()
            all_cards = xmltodict.parse(xml_content)["cockatrice_carddatabase"]["cards"]["card"]

            for index in range(len(all_cards)):
                try:
                    total_cards += 1
                    combined_length_of_all_card_texts += len(all_cards[index]["text"].split())
                except:
                    pass

        print(f'Total cards: {total_cards}')
        print(f'Length of all cards: {combined_length_of_all_card_texts}')
        print(f'Average length: {combined_length_of_all_card_texts / total_cards}')
        print('Done')

    except Exception as e:
        print(f"Exception: {e}")
        print("Usage: python3 average_card_length.py -f filename")


if __name__ == "__main__":
    main()
