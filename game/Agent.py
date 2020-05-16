import numpy as np
from Cards import Deck
class Agent:
    def __init__(self):
        pass
    def action(self):
        """ perform some action? ask to perform some action? """
        pass

class DurakPlayer(Agent):
    """ All a durak player needs is a hand"""
    def __init__(self, deck):
        # Always initialize with an empty deck
        # I.e., create an empty Deck object of same mode as deck
        self.hand = Deck(mode=deck.mode)
        self.hand.empty()

    def drawHand(self, deck, numCards):
        """ Draw variable number of cards from a deck

        :param deck: deck to draw from
        :type deck: Deck
        :param numCards: number of cards to draw
        :type numCards: int
        """
        self.hand.cards += deck.draw(numCards)
