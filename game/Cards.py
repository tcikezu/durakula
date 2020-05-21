import numpy as np
from collections import deque
import random

_CARD_MAP_FULL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D  10', 'D11', 'D12'],
                   ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11'  , 'C12'],
                   ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11'  , 'H12'],
                   ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11'  , 'S12']])
_SUITS = ['Diamonds', 'Clubs', 'Hearts','Spades']
_VALUES = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']

class Card():
    """Map keys: (suit, value) to value (string inside _CARD_MAP_FULL). Additional string method outputs card as 'value' of 'suit' -- e.g., 'Ace' of 'Spades'."""
    def __init__(self, suit: int, value: int):
        self.card = _CARD_MAP_FULL[suit,value]
        self.suit = suit
        self.value = value

    def __repr__(self):
        return self.card

    def __str__(self):
        return _VALUES[self.value] + ' of ' + _SUITS[self.suit]

class CardCollection():
    """First In Last Out collection of Card objects, implemented with collection.deque storing deck order, and np.ndarray representing cards inside the deck."""
    def __init__(self, n_suit: int, n_vals: int, fill=True):
        assert(0 < n_suit <=4 and 0 < n_vals <= 13), 'Deck dimensions out of bounds'
        if fill == True:
            self.deck = deque([Card(s,v) for s in range(n_suit) for v in range(n_vals)])
            self.cards = np.ones((n_suit, n_vals))
        else:
            self.deck = deque()
            self.cards = np.zeros((n_suit, n_vals))
        self.n_suit = n_suit
        self.n_vals = n_vals

    def __repr__(self):
        return repr(self.deck)

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        head = '--- Card Collection ---\n'
        card_str = 'Cards: ' + ','.join([repr(x) for x in self.deck]) +   '.\n'
        size_str = 'Size: ' + str(self.__len__()) + '\n'
        tail = '-----------------------\n'
        return head + card_str + size_str + tail

    def __getitem__(self, idx: int):
        """Get the idx'th card of the deck."""
        return self.deck[idx]

    def __add__(self, other):
        self.cards += other.cards
        self.deck = other.deck + self.deck
        other.empty()
        return self

    def suit(self, idx: int) -> str:
        if 0 <= idx < self.__len__():
            return self.deck[idx].suit
        else:
            return 'Position out of range'

    def value(self, idx: int) -> str:
        if 0 <= idx < self.__len__():
            return self.deck[idx].value
        else:
            return 'Position out of range'

    def empty(self):
        """Empty this deck."""
        self.cards *= 0
        self.order = deque()

    def reorder(self):
        self.deck = deque([Card(idx[0], idx[1]) for idx,v in np.ndenumerate(self.cards) if v == 1])

    def draw_card(self, n=1):
        drawn_cards = CardCollection(n_suits = self.n_suits, n_vals = self.n_vals, fill=False)
        if self.__len__() == 0:
            return drawn_cards
        for i in range(n):
            card = self.order.popleft()
            self.cards[card.suit, card.value] = 0
            drawn_cards[card.suit, card.value] = 1
            drawn_cards.deck.appendleft(card)
        return drawn_cards

    def cut(self, idx=None):
        if idx == None:
            idx = random.randint(0,len(self.deck)-1)
        self.deck.rotate(idx)

class DurakDeck(CardCollection):
    def __init__(self, cards=None, mode='small',fill=True):
        self.mode = mode

        if (mode == 'small'):
            super().__init__(n_suit = 4, n_vals = 9, fill=fill)
        if (mode == 'full'):
            super().__init__(n_suit = 4, n_vals = 13, fill=fill)

        if cards != None:
            self.cards = cards
            self.reorder()

class DurakHand():
    """Initialize a Durak hand by drawing 6 cards from a given deck. The hand itself is 4 x N, N being number of values in input deck. The 0'th row always corresponds to the trump suit."""
    def __init__(self, deck: DurakDeck):
        my_deck = deck.draw_card(6)
        self.hand = np.zeros_like(my_deck.cards)
        self.get_hand_from_deck(my_deck)
        self.trump_idx = deck[-1].suit
        self.trump_suit = deck.suit(-1)
        self.mode = my_deck.mode

    def hand_from_deck(self, deck):
        indices = list(range(deck.n_suits))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        self.hand += deck.cards[indices]

    def deck_from_hand(self) -> DurakDeck:
        indices = list(range(self.hand.shape[0]))
        indices[0], indices[self._trump_idx] = indices[self._trump_idx], indices[0]
        deck = DurakDeck(cards = self.hand[indices], mode = self.mode)
        return deck

class SpadesDeck(CardCollection):
    def __init__(self, fill=True):
        super().__init__(n_suit=4, n_vals=13, fill=fill)
