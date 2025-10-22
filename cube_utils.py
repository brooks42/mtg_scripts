from card import Card

# prints the stats of the cube
def displayStatsForCube(all_cards: list[Card]):
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
    
# rarity is one of "common", "uncommon", "rare", and "mythic"
def cardsWithRarity(cards: list[Card], rarity):
    check = list()

    for card in cards:
        if card.rarity == rarity:
            check.append(card)

    return check

# returns the number of cards in the passed list with the given rarity
def rarityCount(cards, rarity):
    return len(cardsWithRarity(cards, rarity))

# gets the color distribution across all the passed cards
def colorDistributionAmongCards(all_cards: list[Card]):

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

# prunes the cube to a color-balanced 360 cards
# 
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
def dumpCubeFile(cube_list: list[Card], filename: str):
    print(f'Writing {len(cube_list)} cards to cube file...')
    with open(filename, 'w') as f:
        f.write('\n'.join(str(item.name) for item in cube_list))