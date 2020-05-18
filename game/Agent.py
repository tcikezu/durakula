from utils import *
from Cards import DurakDeck
class Agent:
    def __init__(self):
        pass
    def action(self):
        """ perform some action? ask to perform some action? """
        pass

_WAIT = 'MODE_WAIT'
_ATTACK = 'MODE_ATTACK'
_DEFEND = 'MODE_DEFEND'
_FINISHED = 'MODE_FINISHED'
class DurakPlayer(Agent):
    """ All a durak player needs is a hand and an ID."""
    def __init__(self, hand: np.ndarray, player_id: int, trump_idx: int) -> None:
        self._trump_idx = trump_idx
        self.hand = hand
        self.player_id = player_id
        self.player_mode = _WAIT
        self.buffer = np.zeros_like(hand)

    def __str__(self):
        return str(self.player_id) + ':' + str(self.get_deck_from_hand())

    def __len__(self):
        return np.sum(self.hand)

    def clear_buffer(self):
        self.buffer *= 0

    def wait(self):
        self.player_mode = _WAIT
    def attack(self):
        self.player_mode = _ATTACK
    def defend(self):
        self.player_mode = _DEFEND
    def finished(self):
        self.player_mode = _FINISHED

    def is_wait(self):
        return self.player_mode == _WAIT
    def is_attack(self):
        return self.player_mode == _ATTACK
    def is_defend(self):
        return self.player_mode == _DEFEND
    def is_finished(self):
        return self.player_mode == _FINISHED

    def hand_is_empty(self):
        return np.sum(self.hand) == 0

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
