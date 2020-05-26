import numpy as np
from collections import deque
import random
import copy

_CARD_MAP_FULL = np.array([['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
                   ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11'  , 'C12'],
                   ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11'  , 'H12'],
                   ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11'  , 'S12']])
_SUITS = ['Diamonds', 'Clubs', 'Hearts','Spades']
_VALUES = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']

class Card():
    """Map keys: (suit, value) to value (string inside _CARD_MAP_FULL). Additional string method outputs card as 'value' of 'suit' -- e.g., 'Ace' of 'Spades'."""
    def __init__(self, suit_idx: int, value_idx: int):
        self.card = _CARD_MAP_FULL[suit_idx,value_idx]
        self.suit_idx = suit_idx
        self.value_idx = value_idx
        self.suit = _SUITS[suit_idx]
        self.value = _VALUES[value_idx]

    def __repr__(self):
        return self.card

    def __str__(self):
        return self.suit + ' of ' + self.value

class CardCollection():
    """First In Last Out collection of Card objects, implemented with collection.deque storing deck order, and np.ndarray representing cards inside the deck."""
    def __init__(self, n_suits: int, n_vals: int, fill=True):
        assert(0 < n_suits <=4 and 0 < n_vals <= 13), 'Deck dimensions out of bounds'
        if fill == True:
            self.order = deque([Card(s,v) for s in range(n_suits) for v in range(n_vals)])
            self.cards = np.ones((n_suits, n_vals)).astype(int)
        else:
            self.order = deque()
            self.cards = np.zeros((n_suits, n_vals)).astype(int)
        self.n_suits = n_suits
        self.n_vals = n_vals

    def __repr__(self):
        return repr(self.order)

    def __len__(self):
        return len(self.order)

    def __str__(self):
        head = '--- Card Collection ---\n'
        card_str = 'Cards: ' + ','.join([repr(x) for x in self.order]) +   '.\n'
        size_str = 'Size: ' + str(self.__len__()) + '\n'
        tail = '-----------------------\n'
        return head + card_str + size_str + tail

    def __getitem__(self, idx: int):
        """Get the idx'th card of the deck."""
        return self.order[idx]

    def __setitem__(self, idx: int, value: Card): 
        """Set the idx'th card of the deck."""
        self.order[idx] = value

    def __add__(self, other):
        self.cards += other.cards
        self.order = other.deck + self.order
        other.empty()
        return self

    def empty(self):
        """Empty this deck."""
        self.cards *= 0
        self.order = deque()

    def reorder(self):
        self.order = deque([Card(idx[0], idx[1]) for idx,v in np.ndenumerate(self.cards) if v == 1])

    def draw_card(self, n=1):
        # drawn_cards = CardCollection(n_suits = self.n_suits, n_vals = self.n_vals, fill=False)
        drawn_cards = copy.deepcopy(self)
        drawn_cards.empty()
        if self.__len__() == 0:
            return drawn_cards
        for i in range(n):
            card = self.order.popleft()
            self.cards[card.suit_idx, card.value_idx] = 0
            drawn_cards.cards[card.suit_idx, card.value_idx] = 1
            drawn_cards.order.appendleft(card)
        return drawn_cards

    def cut(self, idx=None):
        if idx == None:
            idx = random.randint(0,len(self.order)-1)
        self.order.rotate(idx)

class DurakDeck(CardCollection):
    def __init__(self, cards=None, mode='small',fill=True):
        if (mode == 'small'):
            super().__init__(n_suits = 4, n_vals = 9, fill=fill)
        if (mode == 'full'):
            super().__init__(n_suits = 4, n_vals = 13, fill=fill)

        self.mode = mode
        if cards is not None:
            self.cards = cards
            self.reorder()

    # def draw_card(self, n=1):
    #     drawn_cards = DurakDeck(mode=self.mode, fill=False)
    #     if self.__len__() == 0:
    #         return drawn_cards
    #     for i in range(n):
    #         card = self.order.popleft()
    #         self.cards[card.suit, card.value] = 0
    #         drawn_cards.cards[card.suit, card.value] = 1
    #         drawn_cards.order.appendleft(card)
    #     return drawn_cards

class DurakHand():
    """Initialize a Durak hand by drawing 6 cards from a given deck. The hand itself is 4 x N, N being number of values in input deck. The 0'th row always corresponds to the trump suit."""
    def __init__(self, deck: DurakDeck):
        my_deck = deck.draw_card(6)
        self.hand = np.zeros_like(my_deck.cards).astype(int)
        self.trump_idx = deck[-1].suit_idx
        self.trump_suit = deck[-1].suit
        self.get_hand_from_deck(my_deck)
        self.mode = my_deck.mode

    def get_hand_from_deck(self, deck):
        indices = list(range(deck.n_suits))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        self.hand += deck.cards[indices]
        return self.hand

    def get_deck_from_hand(self) -> DurakDeck:
        indices = list(range(self.hand.shape[0]))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        deck = DurakDeck(cards = self.hand[indices], mode = self.mode)
        return deck

    # def __getitem__(self, key):
    #     return self.hand[key[0],key[1]]

    # def __setitem__(self, key, value):
    #     self.hand[key[0], key[1]] = value

class SpadesDeck(CardCollection):
    def __init__(self, fill=True):
        super().__init__(n_suits=4, n_vals=13, fill=fill)
