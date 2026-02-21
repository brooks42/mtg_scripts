#!/usr/bin/env python

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
                        self.legal = prop.string == 'legal' or prop.string == 'limited' or prop.string == 'restricted'
            
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
    