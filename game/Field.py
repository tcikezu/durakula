from math import ceil
import numpy as np
from utils import indices_of_ones


class Field:
    """Abstract field class. Create rules of the field here."""
    def __init__(self):
    	pass
    def __str__(self):
    	pass
    def get_legal_moves(self):
    	pass
    def list_moves(self):
    	pass
    def has_legal_moves(self):
    	pass
    def execute_move(self):
    	pass

    # @staticmethod
    # def _increment_move(move):
    # 	""" Generator expression for incrementing moves """

# _ACTION_WAIT = 'ACTION_WAIT'
# _ACTION_ATTACK = 'ACTION_ATTACK'
_ACTION_GIVEUP = 'ACTION_GIVEUP'

class DurakField(Field):
    """This class defines legal moves you can make in a game of Durak, given every players' hands and the current cards played on the field."""
    # Might be useful to convert this into **kwargs
    def __init__(self, deck, players, first_player_id):
        """Inits DurakField with deck and players."""
        self.n_vals = deck.n_vals
        self.n_suits = deck.n_suits
        self.drawing_deck = deck
        self.trump_suit = self.drawing_deck[-1].suit

        self.players = players
        self.attack_order = []

        self.first_attack = True
        self.is_active = True

        # Field is a 6 x n_suit x n_val array.
        # Field is divided into 2 buffer layers, and one active layer.
        # The 2 buffer layers correspond to attack and defend cards that have been paired on the table.
        # The active layer corresponds to any attack card that is awaiting a defense pair.
        # The final layer is a bunch of ones multiplied by the player id that is executing a move.

        self.field_state = np.zeros((6, self.n_suits, self.n_vals))
        self.attack_buffer = self.field[0,:,:]
        self.defense_buffer = self.field[1,:,:]
        self.attacks = self.field[2,:,:]

        self.set_first_attack(self.first_attack)
        self._set_number_cards()

    def __str__(self):
        """Output string for Field."""

        head = '--- Playing Field ---\n'
        drawing_deck_str = 'Drawing DurakDeck: ' + str(self.drawing_deck) + '\n'
        player_str = [str(self.players)]
        trump_str = 'Trump suit is ' + self.trump_suit + '\n'
        tail = '---------------------\n'
        return head + drawing_deck_str + ''.join(player_str_list) + trump_str + tail

    def set_first_attack(self, first_attack):
        """Boolean layer that is all 1's if this is indeed the first attack, and all 0's
        if not."""
        self.first_attack = first_attack
        self.field_state[3,:,:] = self.first_attack

    def _set_number_cards(self):
        """Encode the number of cards left in the deck (from which we draw new cards -- hence drawing_deck.)
        This will look like a bunch of 0's followed by a bunch of 1's -- sorting
        allows us to get rid of all suit / value information."""
        self.field_state[4,:,:] = np.sort(np.sort(self.drawing_deck.cards,axis=0),axis=1)

    def clear_field(self):
        """Clear field after a defender has successfully defended or given up. Make all that aren't finished in wait mode."""
        self.attack_buffer *= 0
        self.defense_buffer *= 0
        self.attacks *= 0
        self.set_first_attack(True)
        self._set_number_cards()
        for player_id in range(self.players.n_players):
            if self.players.is_finished(player_id) == False:
                self.players.clear_buffer(player_id)
                self.players.wait(player_id)
        self.is_active = True
        self.attack_order = []

    def get_legal_moves(self, player_id) -> list:
        """Returns a list of legal moves. The basic moves are to attack and to defend. If player mode is set to finished or wait, then no move can be performed. A player in defense can always give up. If first attack, then attack must be performed."""
        if self.players.is_defend(player_id):
            # Assuming there are attacks in self.attacks
            attack_idxs = np.flatnonzero(self.attacks)

            # Successful defense -- nobody attacks.
            if len(attack_idxs) == 0:
                return [()]

            nontrump_attack_idxs = attack_idxs[attack_idxs >= self.n_vals]
            valid_defenses = np.zeros((self.drawing_deck.cards.size, self.drawing_deck.cards.size))

            f = lambda x : (x // self.n_vals + 1)*self.n_vals # Compute the suit ceil - ie, 13, 26, 39, 52 depending on x's suit.

            # All cards that are the same suit, higher value than those of attacks.
            for att_idx in attack_idxs:
                valid_defenses[att_idx + 1 : f(att_idx), att_idx] = 1
                # All trump cards
                if att_idx in nontrump_attack_idxs:
                    valid_defenses[:self.n_vals, att_idx] = 1

            # All cards of same value as attacks.
            if self.first_attack:
                valid_defenses[att_idx % self.n_vals : att_idx % self.n_vals + self.n_suits*self.n_vals : self.n_vals, att_idx] = 1

            valid_defenses *= self.players.hands[player_id].ravel()[:,np.newaxis] # Mask by player's hand
            list_def_combinations = self.defense_combinations(valid_defenses)# Compute all possible defend moves.
            return list_def_combinations

        elif self.players.is_attack(player_id):
            # Attacks with respect to cards on self.field.
            valid_attacks = np.zeros_like(self.attacks)
            defense_id = self.players.player_in_defense()

            if self.first_attack:
                valid_attacks = self.players.hands[player_id] # For first attack, entire hand is valid.
                L = min(np.sum(valid_attacks), self.players.get_len(defense_id)) # Cannot attack with more than what the defender has.
                return self.first_attack_combinations(valid_attacks, L) # Note: if first attack, then not attacking is not an option.
            else:
                # Add all card values from attack and defense buffers to valid_attacks.
                buffer_idxs = indices_of_ones(self.attack_buffer + self.defense_buffer)
                valid_attacks = np.zeros_like(self.attacks)

                for idx in buffer_idxs:
                    valid_attacks[:,idx[1]] = 1 # Must have same value as those in buffer.

                valid_attacks *= self.players.hands[player_id]# Mask with player's hand.
                # Cannot attack with more than what the defender has.
                L = min(np.sum(valid_attacks), self.players.get_len(defense_id))
                # Note - if not first attack, then one can choose to not attack. Valid attacks are any number of cards whose value matches that on the table.
                return list_nonzero_combinations(valid_attacks, L) + [()]

        elif self.players.is_wait(player_id) or self.players.is_finished(player_id):
            return []
        else:
            raise ValueError('INVALID PLAYER MODE')

    def first_attack_combinations(self, valid_attacks: np.ndarray, L: int) -> list:
        """The first attack can only be cards of the same value."""
        idxs = indices_of_ones(valid_attacks)
        def valid(c):
            """The very first attack must be with cards of same value."""
            return min(np.array(c)[:,1]) == max(np.array(c)[:,1])

        first_att_combinations = []
        for r in range(1,L+1):
            first_att_combinations += [c for c in combinations(idxs, r) if valid(c)]
        return first_att_combinations

    def defense_combinations(self, valid_defenses: np.ndarray) -> list:
        """Returns every possible defense given valid_defenses."""
        idxs = indices_of_ones(valid_defenses)
        # Base case - there is no defense we can do.
        if len(idxs) == 0:
            return [_ACTION_GIVEUP]

        attacks = np.unique(np.argwhere(valid_defenses)[:,1])
        defenses = np.unique(np.argwhere(valid_defenses)[:,0])
        # Base case - can't use the same card to defend multiple attacks.
        if len(attacks) > len(defenses):
            return [_ACTION_GIVEUP]

        # Base case - can't reduce the number of attacks
        if np.sum(self.attacks) > len(attacks):
            return [_ACTION_GIVEUP]

        def valid(c):
            """A valid defense move is one where the number of unique defend cards equals the number of unique attack cards."""
            return len(np.unique(np.array(c)[:,0])) == len(np.unique(np.array(c)[:,1])) == len(c)

        r = len(attacks)
        def_combinations = [_ACTION_GIVEUP]
        def_combinations += [c for c in combinations(idxs, r) if valid(c)]
        return def_combinations

    def has_legal_moves(self, player_id: int) -> bool:
        """A player has legal moves so long as their hand isn't empty."""
        return self.players.hand_is_empty(player_id)

    def execute_move(self, move, player_id: int) -> None:
        """Execute a move for the given player. Evaluates whether the player has finished their game (ie run out of cards) at the end of move."""
        if self.players.is_attack(player_id):
            current_buffer = np.zeros_like(self.players.buffers[player_id])
            if len(move) == 0: # Wait.
                pass
            else:
                self.attack_order.append(player_id)
                for m in move:
                    current_buffer[m] = 1
                self.players.buffers[player_id] += current_buffer
                self.attacks += current_buffer
                self.players.hands[player_id] -= current_buffer
        elif self.players.is_defend(player_id):
            current_buffer = np.zeros_like(self.players.buffers[player_id])
            if len(move) == 0: # Nothing to defend.
                # A successful defense occured.
                if len(self.players.players_in_attack()) == 0:
                    self.is_active = False
                # The defense continues.
                else:
                    self.is_active = True
                    self.attack_buffer += self.attacks
                    self.attacks *= 0
            elif move == _ACTION_GIVEUP:
                self.players.hands[player_id] += self.attacks + self.attack_buffer + self.defense_buffer
                self.is_active = False
            else: # The defense continues.
                for m in move:
                    current_buffer[m[0] // self.n_vals, m[0] % self.n_vals] = 1
                self.players.hands[player_id] -= current_buffer
                self.players.buffers[player_id] += current_buffer
                self.attack_buffer += self.attacks
                self.defense_buffer += current_buffer
                self.attacks *= 0

        elif self.players.is_wait(player_id):
            pass
        elif self.players.is_finished(player_id):
            pass

        # Note - even if there are cards remaining, an empty hand at end of round means you've finished play.
        if self.players.hand_is_empty(player_id):
            if self.players.is_defend(player_id):
                self.is_active = False
            self.players.finished(player_id)

    @staticmethod
    def _increment_move(move):
        """ Generator expression for incrementing moves """
        pass
