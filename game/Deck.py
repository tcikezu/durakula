"""
Deck.py
===============
Deck module.
"""
from Card import Card

class Deck:
    """A Deck is an object that contains a collection of Cards.

    Attributes:
        mode (str): A string to set the length of starting deck. This is
        either 'full' or 'small'.

    """

    def __init__(self, mode='full'):
        """
        Args:
            mode (str): 'full' or 'small`

        """
        self.mode = None
        self.deck = []
        self.set_mode(mode)
        self._get_cards()

    def __str__(self):
        """Prints the entire deck."""
        card_names = []
        for c in self.deck:
            card_names.append(c.__str__())
        return ' '.join(card_names)

    def __len__(self):
        """ Returns the length of the current deck."""
        return len(self.deck)

    def set_mode(self, mode):
        """ Sets the mode of the deck.

        Args:
            mode (str): 'full' or 'small'. Corresponds to playing with
            52 cards or cards above 5 in value (of every suit).

        """
        assert mode in set(['full', 'small'])
        self.mode = mode

    def build_deck(self, suits, values):
        """ Method which adds Card objects to deck, to create a
        complete deck of our Deck object."""
        for s in suits:
            for v in values:
                self.deck.append(Card(s, v))

    def _get_cards(self):
        """ Private method to build the deck given mode"""
        if self.mode == 'full':
            suits = ['S', 'C', 'H', 'D']
            values = range(2, 15)

        elif self.mode == 'small':
            suits = ['S', 'C', 'H', 'D']
            values = range(6, 15)

        else:
            raise Exception('Invalid Deck Type.')
        self.build_deck(suits, values)

