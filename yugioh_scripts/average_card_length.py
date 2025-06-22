
        # "englishAttribute": "earth", 
        # "name": "Gimmick Puppet Gear Changer", 
        # "localizedAttribute": "EARTH", 
        # "type": "monster", 
        # "level": 1, 
        # "atk": 100, 
        # "properties": [
        #     "Machine", 
        #     "Effect"
        # ], 
        # "effectText": "Cannot be Special Summoned from the Deck. Once per turn: You can target 1 \"Gimmick Puppet\" monster you control, except this card; this card's Level becomes the Level of that monster.", 
        # "id": 10692, 
        # "def": 100

    # {
    #     "englishAttribute": "spell", 
    #     "name": "Mystical Space Typhoon", 
    #     "localizedAttribute": "SPELL", 
    #     "type": "spell", 
    #     "englishProperty": "quickplay", 
    #     "localizedProperty": "Quick-Play", 
    #     "effectText": "Target 1 Spell/Trap on the field; destroy that target.", 
    #     "id": 4909
    # }, 

    # {
    #     "englishAttribute": "trap", 
    #     "name": "Dark Bribe", 
    #     "localizedAttribute": "TRAP", 
    #     "type": "trap", 
    #     "englishProperty": "counter", 
    #     "localizedProperty": "Counter", 
    #     "effectText": "When your opponent activates a Spell/Trap Card: Your opponent draws 1 card, also negate the Spell/Trap activation, and if you do, destroy it.", 
    #     "id": 7349
    # }, 

    # {
    #     "englishAttribute": "light", 
    #     "name": "Number C39: Utopia Ray V", 
    #     "localizedAttribute": "LIGHT", 
    #     "type": "monster", 
    #     "atk": 2600, 
    #     "rank": 5, 
    #     "properties": [
    #         "Warrior", 
    #         "Xyz", 
    #         "Effect"
    #     ], 
    #     "effectText": "3 Level 5 monsters\nWhen this card in its owner's possession is destroyed by an opponent's card: You can target 1 Xyz Monster in your GY; return that target to the Extra Deck. If this card has a \"Utopia\" monster as material, it gains this effect.\n\u25cfOnce per turn: You can detach 1 material from this card, then target 1 monster your opponent controls; destroy that monster, and if it was face-up, inflict damage to your opponent equal to the ATK the destroyed monster had on the field.", 
    #     "id": 10569, 
    #     "def": 2000
    # }, 

    # {
    #     "englishAttribute": "light", 
    #     "name": "Odd-Eyes Arcray Dragon", 
    #     "pendEffect": "If you have 2 cards in your Pendulum Zones: You can Special Summon this card, then you can apply this effect.\n\u25cfShuffle 1 card from your Pendulum Zone into the Deck, then if it was added to your Extra Deck, you can Special Summon it, ignoring its Summoning conditions. You can only use this effect of \"Odd-Eyes Arcray Dragon\" once per turn.", 
    #     "localizedAttribute": "LIGHT", 
    #     "type": "monster", 
    #     "level": 12, 
    #     "atk": 4000, 
    #     "properties": [
    #         "Dragon", 
    #         "Fusion", 
    #         "Pendulum", 
    #         "Effect"
    #     ], 
    #     "pendScale": 13, 
    #     "effectText": "4 Dragon monsters (1 Fusion, 1 Synchro, 1 Xyz, and 1 Pendulum)\n(This card is always treated as \"Supreme King Z-ARC\".)\nThis face-down card in the Extra Deck must first be either Fusion Summoned, or Special Summoned by Tributing 1 Level 12 DARK \"Supreme King Z-ARC\". If this card is Special Summoned from the Extra Deck: You can place 1 Pendulum Monster from your Deck in your Pendulum Zone. If this card in the Monster Zone is destroyed: You can place this card in your Pendulum Zone.", 
    #     "id": 19172, 
    #     "def": 4000
    # }, 

import os
import json

def printCoolStatsForFile(filename):
    with open(filename, 'r') as file:
        try:
            data = json.load(file)

            effect_lengths = []

            all_cards = 0
            normal_monsters = 0
            effect_monsters = 0
            fusion_monsters = 0
            xyz_monsters = 0
            synchro_monsters = 0
            pendulum_monsters = 0
            link_monsters = 0

            effect_monsters_total_length = 0
            pendulum_monsters_total_length = 0

            spell_cards = 0
            spell_card_total_length = 0

            trap_cards = 0
            trap_card_total_length = 0
            
            for card in data:

                all_cards += 1

                if card["type"] == "monster":
                    if card["properties"] != None:
                        if "Effect" in card["properties"]:

                            # pendulums are a special case since they have a "pendEffect" property
                            if "Pendulum" in card["properties"]:
                                pendEffect = ""

                                try:
                                    pendEffect = card["pendEffect"]
                                except:
                                    # this is fine, just a pendulum monster with no pend effect
                                    pass

                                pend_word_count = len(card["effectText"].split()) + len(pendEffect.split())

                                effect_lengths.append(card["effectText"].split() + pendEffect.split())
                                effect_monsters += 1
                                pendulum_monsters += 1
                                effect_monsters_total_length += pend_word_count
                                pendulum_monsters_total_length += pend_word_count

                            else:
                                effect_lengths.append(card["effectText"].split())
                                effect_monsters += 1
                                effect_monsters_total_length += len(card["effectText"].split())

                            if "Xyz" in card["properties"]:
                                xyz_monsters += 1
                            if "Fusion" in card["properties"]:
                                fusion_monsters += 1
                            if "Synchro" in card["properties"]:
                                synchro_monsters += 1
                            if "Link" in card["properties"]:
                                link_monsters += 1

                        else:
                            normal_monsters += 1
                            effect_lengths.append(0) # track it for averaging later

                elif card["type"] == "spell":
                    effect_lengths.append(card["effectText"].split())
                    spell_card_total_length += len(card["effectText"].split())
                    spell_cards += 1
                elif card["type"] == "trap":
                    effect_lengths.append(card["effectText"].split())
                    trap_card_total_length += len(card["effectText"].split())
                    trap_cards += 1
                else:
                    print(f"found a card with an unknown type: {card}")

            print(f"Card count: {all_cards}")
            print(f"Normal monsters: {normal_monsters}")
            print(f"Effect monsters: {effect_monsters}")
            print(f"Spells: {spell_cards}")
            print(f"Traps: {trap_cards}")

            print(f"Fusions: {fusion_monsters}")
            print(f"Xyzs: {xyz_monsters}")
            print(f"Synchros: {synchro_monsters}")
            print(f"Pendulums: {pendulum_monsters}")
            print(f"Links: {link_monsters}")

            average_length_of_all_cards = (effect_monsters_total_length + trap_card_total_length + spell_card_total_length) / (effect_monsters + trap_cards + spell_cards)

            print(f"Total words in all of yugioh: {effect_monsters_total_length + trap_card_total_length + spell_card_total_length}")
            print(f"Combined card count for non-Normal Monster cards: {effect_monsters + trap_cards + spell_cards} (+{normal_monsters})")
            print(f"Average length of all cards: {average_length_of_all_cards: .2f}")

        except Exception as e:
            print(f"Exception happened: {e}")


if __name__ == "__main__":
    input_file = "yugioh_cards.json"
    printCoolStatsForFile(input_file)
