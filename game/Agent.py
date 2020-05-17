import numpy as np
from Cards import Deck, durak_hand, normal_hand
class Agent:
    def __init__(self):
        pass
    def action(self):
        """ perform some action? ask to perform some action? """
        pass

# DurakPlayer a collection?
class DurakPlayer(Agent):
    """ All a durak player needs is a hand"""
    def __init__(self, deck: Deck, trumpSuit: str) -> None:
        # Always initialize with an empty deck
        # I.e., create an empty Deck object of same mode as deck
        self.trumpSuit = trumpSuit
        self.hand = durak_hand(deck, trumpSuit)
        self.mode = 'waiting'

    def drawFromDeck(self, deck, numCards):
        """ Draw variable number of cards from a deck

        :param deck: deck to draw from
        :type deck: Deck
        :param numCards: number of cards to draw
        :type numCards: int
        """
        self.deck += deck.drawCard(numCards)
        self.hand = durak_hand(self.deck)

    def attack(self):
        self.mode = 'attack'

    def defend(self):
        self.mode = 'defend'
