from utils import *
from Cards import DurakHand
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
class DurakPlayer(DurakHand):
    """ All a durak player needs is a hand and an ID."""
    def __init__(self, deck, player_id: int) -> None:
        super().__init__(deck) 
        self.player_id = player_id
        self.player_mode = _WAIT
        self.buffer = np.zeros_like(self.hand)

    def __str__(self):
        return str(self.player_id) + ':' + str(self.get_deck_from_hand())

    def __len__(self):
        return np.sum(self.hand)

    def clear_buffer(self):
        """Remove all cards from the buffer hand."""
        self.buffer *= 0

    def wait(self) -> None:
        """Change player mode to wait."""
        self.player_mode = _WAIT
    def attack(self) -> None:
        """Change player mode to attack."""
        self.player_mode = _ATTACK
    def defend(self) -> None:
        """Change player mode to defend."""
        self.player_mode = _DEFEND
    def finished(self) -> None:
        """Change player mode to finished."""
        self.player_mode = _FINISHED

    def is_wait(self) -> bool:
        return self.player_mode == _WAIT
    def is_attack(self) -> bool:
        return self.player_mode == _ATTACK
    def is_defend(self) -> bool:
        return self.player_mode == _DEFEND
    def is_finished(self) -> bool:
        return self.player_mode == _FINISHED

    def hand_is_empty(self) -> bool:
        return np.sum(self.hand) == 0

    def manual_action(self) -> None:
        action = None
        while(action == None):
            if self.is_defend():
                action = input("Select an action: 0 - defend, 1 - pass.")
            if self.is_attack():
                action = input("Select an action: 0 - attack, 1 - pass.")

            if action != 0 or action != 1:
                action = None
        card = None
        if action == 0:
            card = self.select_card()
        elif action == 1:
            return
        else:
            return

    def select_card(self) -> str:
        card = input('Select a card: (<SUIT><VALUE>)')
        return card
