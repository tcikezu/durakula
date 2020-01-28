"""
Card.py
==================
Card module.
"""
class Card:
    """ Card class """
    def __init__(self, suit, value):
        self.suit = None
        self.value = None
        self.set_suit(suit)
        self.set_value(value)

    def __str__(self):
        return self.suit + str(self.value)

    def set_suit(self, suit):
        assert suit in set(['S', 'H', 'C', 'D'])
        self.suit = suit

    def set_value(self, value):
        assert value in set(range(2, 14 + 1))
        self.value = value
