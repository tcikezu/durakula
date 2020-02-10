"""
Card.py
==================
Card Module.
"""
class Card:
    """ Card has public attributes suit and value, from which we form
     card games.

    Attributes:
        suit (str): Representing (D)iamond, (C)lub, (H)eart, (S)pades.
        value (int): Representing 2 through Ace (14).

    """
    def __init__(self, suit, value):
        """Initialize and create the card."""
        self.suit = None
        self.value = None
        self.set_suit(suit)
        self.set_value(value)

    def __str__(self):
        return self.suit + str(self.value)

    def set_suit(self, suit):
        """ The suit of the card is set here. """
        assert suit in set(['S', 'H', 'C', 'D'])
        self.suit = suit

    def set_value(self, value):
        """ Value of card set here. """
        assert value in set(range(2, 14 + 1))
        self.value = value
