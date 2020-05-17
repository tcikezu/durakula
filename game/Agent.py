import numpy as np
from Cards import DurakDeck
class Agent:
    def __init__(self):
        pass
    def action(self):
        """ perform some action? ask to perform some action? """
        pass

class DurakPlayer(Agent):
    """ All a durak player needs is a hand and an ID."""
    def __init__(self, hand: np.ndarray, player_id: int, trump_idx: int) -> None:
        self._trump_idx = trump_idx
        self.hand = hand
        self.player_id = player_id
        self.player_mode = 'waiting'

    def __str__(self):
        return str(self.player_id) + ':' + str(self.get_deck_from_hand())

    def attack(self):
        self.player_mode = 'attack'

    def defend(self):
        self.player_mode = 'defend'

    def finish(self):
        assert(np.sum(self.hand) == 0)
        self.player_mode = 'finished'

    def wait(self):
        self.player_mode = 'waiting'

    def get_deck_from_hand(self) -> DurakDeck:
        """Convert a hand into a deck object.

        Returns:
            deck (DurakDeck): A `DurakDeck` instance, populated with cards inside the hand.
        """
        indices = list(range(self.hand.shape[0]))
        indices[0], indices[self._trump_idx] = indices[self._trump_idx], indices[0]
        if self.hand.size == 52:
            deck = DurakDeck(cards = self.hand[indices], mode = 'full')
        elif self.hand.size == 36:
            deck = DurakDeck(cards = self.hand[indices], mode = 'small')
        else:
            raise ValueError('INVALID HAND SIZE')
        return deck
