import numpy as np
import random
from collections import deque

_CARD_MAP_FULL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
                 ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'],
                 ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12'],
                 ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12']])

_CARD_MAP_SMALL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                 ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                 ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'],
                 ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']])
_SUITS = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
_VALUES = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

class CardCollection:
    def __init__(self, n_suits=4, n_vals=9, fill=False):
        if fill:
            self.cards = np.ones((n_suits, n_vals)).astype(int)
        else:
            self.cards = np.zeros((n_suits, n_vals)).astype(int)
        self.order = deque([i for i, v in np.ndenumerate(self.cards) if v == 1])

    def __getitem__(self, idx):
        if self.mode == 'full':
            return _CARD_MAP_FULL[self.order[idx]]
            # return self.cards[self.order[idx]]
        elif self.mode == 'small':
            return _CARD_MAP_SMALL[self.order[idx]]
            # return self.cards[self.order[idx]]
        else:
            ValueError('INVALID MODE')

    def __setitem__(self, idx, value):
        self.cards[self.order[idx]] = value
        if value == 1:
            self.order.appendleft(self.order[idx])
        elif value == 0:
            self.order.remove(self.order[idx])
        else:
            ValueError('INVALID VALUE (MUST BE 0 OR 1)')

    def __eq__(self, other):
        self.cards = other.cards
        self.order = other.order

    def __add__(self, other):
        self.cards += other.cards
        self.order += other.order
        assert(self.cards.all() == 0 or self.cards.all() == 1), 'Oops! we have 2 or more of the same card.'
        return self

    # def __iter__(self):
    #     if self.mode == 'full':
    #         yield from _CARD_MAP_FULL[self.order]
    #     else:
    #         yield from _CARD_MAP_SMALL[self.order]

    # def __next__(self):
    #     pass
    def __len__(self):
        return int(np.sum(self.cards))

    def __str__(self):
        head = '--- Card Collection ---\n'
        card_str = 'Cards: ' + ','.join(_CARD_MAP_SMALL[self.cards.astype(bool)]) + '.\n'
        size_str = 'Size: ' + str(self.__len__()) + '\n'
        tail = '-----------------------\n'
        return head + card_str + size_str + tail

    def suit(self, idx):
        return _SUITS[self.order[idx][0]]

    def value(self, idx):
        return _VALUES[self.order[idx][1]]

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
        self.order = deque()
        return self

    def shuffle(self):
        random.shuffle(self.order)

    def draw_card(self,n=1):
        """Draw (ie, pop) according to an order."""
        #drawn_card = np.zeros((self.n_suits, self.n_vals)).astype(int)
        drawn_card = Deck(mode = self.mode)
        drawn_card.empty()
        for i in range(n):
            idx = self.order[0]
            self.__setitem__(0, 0)
            drawn_card.cards[idx] = 1
            drawn_card.order.appendleft(idx)
        return drawn_card

    # idx notation confusing -- here it means the specific card
    # but in other cases idx refers to a position in self.order
    def add_card(self, idx):
        self.cards[idx] = 1
        self.order.appendleft(idx)
        return self

    def remove_card(self, idx=0):
        self.cards[idx] = 0
        self.order.removeleft(idx)
        return self

class Deck(CardCollection):
    """Create a card collection, in either small or full mode."""
    def __init__(self, mode='small'):
        self.mode = mode
        self.n_suits = None
        self.n_vals = None
        self._apply_mode()
        super().__init__(n_suits=self.n_suits, n_vals=self.n_vals, fill=True)
