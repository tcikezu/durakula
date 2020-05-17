import numpy as np
from Cards import Deck
class Agent:
    def __init__(self):
        pass
    def action(self):
        """ perform some action? ask to perform some action? """
        pass

# DurakPlayer a collection?
class DurakPlayer(Agent):
    """ All a durak player needs is a hand"""
    def __init__(self, hand: np.ndarray) -> None:
        # Always initialize with an empty deck
        # I.e., create an empty Deck object of same mode as deck
        self.hand = hand
        self.mode = 'waiting'

    def attack(self):
        self.mode = 'attack'

    def defend(self):
        self.mode = 'defend'

    def finish(self):
        assert(np.sum(self.hand) == 0)
        self.mode = 'finished'

    def wait(self):
        self.mode = 'waiting'
