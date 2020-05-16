import numpy as np
import random

_CARD_MAP_FULL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
                 ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'],
                 ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12'],
                 ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12']])

_CARD_MAP_SMALL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                 ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                 ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'],
                 ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']])
_SUITS = ['Diamonds', 'Clubs', 'Hearts', 'Spades']

class CardCollection:
    def __init__(self, n_suits=4, n_vals=9, fill=False):
        if fill:
            self.cards = np.ones((n_suits, n_vals)).astype(int)
        else:
            self.cards = np.zeros((n_suits, n_vals)).astype(int)

    def __len__(self):
        return int(np.sum(self.cards))

    def __str__(self):
        head = '--- Card Collection ---\n'
        card_str = 'Cards: ' + ','.join(_CARD_MAP_SMALL[self.cards.astype(bool)]) + '.\n'
        size_str = 'Size: ' + str(self.__len__()) + '\n'
        tail = '-----------------------\n'
        return head + card_str + size_str + tail


class Deck(CardCollection):
    """ Create a card collection, in either small or full mode"""
    def __init__(self, mode='small'):
        self.mode = mode
        self.n_suits = None
        self.n_vals = None
        self._apply_mode()
        super().__init__(n_suits=self.n_suits, n_vals=self.n_vals, fill=True)

    def _apply_mode(self):
        if self.mode == 'full':
            self.n_suits = 4
            self.n_vals = 13
        elif self.mode == 'small':
            self.n_suits = 4
            self.n_vals = 9

    def empty(self):
        """ Empty this deck. """
        self.cards *= 0

    def draw(self, n=1):
        """Draw a random card."""
        rand_idx = np.array(random.sample(np.argwhere(self.cards==1).tolist(), k=n))
        drawn_card = np.zeros((self.n_suits, self.n_vals)).astype(int)
        drawn_card[rand_idx[:,0], rand_idx[:,1]] = 1
        self.cards[rand_idx[:,0], rand_idx[:,1]] = 0
        return drawn_card
