from utils import *
import copy
from math import ceil

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
    def __init__(self, deck, players):
        """Inits DurakField with deck and players."""
        self.n_vals = deck.n_vals
        self.n_suits = deck.n_suits
        self.drawing_deck = deck
        self.n_players = len(players)
        self.players = players # list of Agent class objects
        self.trump_suit = self.drawing_deck[-1].suit
        self.trump_suit_idx = deck.order[-1].suit_idx
        self.attack_order = []

        self.first_attack = True
        self.field_active = True

        # field is a N x N array, where N = number of cards
        # columns are attacks
        # rows are defends
        # the first row of attacks and defends is always the trump suit
        # the first 13 rows and 13 columns of field also correspond to trump suit
        self.field = np.zeros((deck.cards.size, deck.cards.size))
        # self.field_buffer = np.zeros_like(self.field)
        self.attacks = np.zeros_like(deck.cards)
        self.attack_buffer = np.zeros_like(self.attacks)

    def __str__(self):
        """Output string for Field."""

        head = '--- Playing Field ---\n'
        drawing_deck_str = 'Drawing DurakDeck: ' + str(self.drawing_deck) + '\n'
        player_str_list = [str(player)+'\n' for player in self.players]
        trump_str = 'Trump suit is ' + self.trump_suit + '\n'
        tail = '---------------------\n'
        return head + drawing_deck_str + ''.join(player_str_list) + trump_str + tail

    def field_is_empty(self) -> bool:
        """Returns whether the field is empty."""
        return np.sum(self.field).astype('int') == 0

    def clear_field(self):
        """Clear field after a defender has successfully defended or given up. Make all that aren't finished in wait mode."""
        self.field *= 0
        self.attacks *= 0
        self.attack_buffer *= 0
        for p in self.players:
            if p.is_finished() == False:
                p.clear_buffer()
                p.wait()
        self.first_attack = True
        self.field_active = True
        self.attack_order = []

    def player_in_defense(self):
        """Returns the player that is currently defending."""
        return [p for p in self.players if p.is_defend()][0]

    def players_in_attack(self) -> list:
        """Returns a list of players that are attacking."""
        return [p for p in self.players if p.is_attack()]

    def get_legal_moves(self, player_id: int) -> list:
        """Returns a list of legal moves. The basic moves are to attack and to defend. If player mode is set to finished or wait, then no move can be performed. A player in defense can always give up. If first attack, then attack must be performed."""
        player = self.players[player_id]
        if player.is_defend():
            # Assuming there are attacks in self.attacks
            attack_idxs = np.flatnonzero(self.attacks) # use flatnonzero or argwhere

            # Successful defense -- nobody attacks.
            if len(attack_idxs) == 0:
                return [()]

            nontrump_attack_idxs = attack_idxs[attack_idxs >= self.n_vals]
            valid_defenses = np.zeros_like(self.field)
            f = lambda x : (x // self.n_vals + 1)*self.n_vals# Compute the suit ceil -- ie, 13, 26, 39, 52 depending on x's suit
            # All cards that are same suit, higher value than those of attacks.
            for att_idx in attack_idxs:
                valid_defenses[att_idx + 1 : f(att_idx), att_idx] = 1
            # All trump cards
            for att_idx in nontrump_attack_idxs:
                valid_defenses[:self.n_vals, att_idx] = 1

            # All cards of same value as attacks.
            if self.first_attack:
                valid_defenses[att_idx % self.n_vals : att_idx % self.n_vals + self.n_suits*self.n_vals : self.n_vals, att_idx] = 1
            valid_defenses *= player.hand.ravel()[:,np.newaxis] # Mask with player's hand.
            list_def_combinations = self.defense_combinations(valid_defenses)# Compute all possible defend moves.
            return list_def_combinations

        elif player.is_attack():
            # Attacks with respect to cards on self.field.
            valid_attacks = np.zeros_like(self.attacks)

            if self.first_attack:
                # For first attack, entire hand is valid.
                valid_attacks = player.hand
                # Cannot attack with more than what the defender has.
                L = min(np.sum(valid_attacks), len(self.player_in_defense()))
                # Note: if first attack, then not attacking is not an option.
                return self.first_attack_combinations(valid_attacks, L)

            else:
                # Add all values on the table to valid_attacks.
                attack_idxs = np.append(np.argwhere(self.field)[:,1], np.argwhere(self.field)[:,0])
                valid_attacks[:,attack_idxs % self.n_vals] = 1
                valid_attacks *= player.hand # Mask with player's hand.
                # Cannot attack with more than what the defender has.
                L = min(np.sum(valid_attacks), len(self.player_in_defense()))
                # Note - if not first attack, then one can choose to not attack. Valid attacks are any number of cards whose value matches that on the table.
                return list_nonzero_combinations(valid_attacks, L) + [()]

        elif player.is_wait() or player.is_finished():
            return []
        else:
            raise ValueError('INVALID PLAYER MODE')

    def first_attack_combinations(self, valid_attacks: np.ndarray, L: int) -> list:
        """The first attack can only be cards of the same value."""
        idxs = indices_of_ones(valid_attacks)
        def valid(c):
            """Mini-function that only serves to create valid combinations."""
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
        defends = np.unique(np.argwhere(valid_defenses)[:,0])
        # Base case - can't use the same card to defend multiple attacks.
        if len(attacks) > len(defends):
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
        return self.players[player_id].hand_is_empty()

    def execute_move(self, move, player_id: int) -> None:
        """Execute a move for the given player. Evaluates whether the player has finished their game (ie run out of cards) at the end of move."""
        player = self.players[player_id]
        if player.is_attack():
            current_buffer = np.zeros_like(player.buffer)
            if len(move) == 0: # Wait.
                # player.wait()
                pass
            else:
                self.attack_order.append(player_id)
                for m in move:
                    current_buffer[m] = 1
                player.buffer += current_buffer
                self.attacks += current_buffer
                player.hand -= current_buffer
        elif player.is_defend():
            current_buffer = np.zeros_like(player.buffer)
            if len(move) == 0: # Nothing to defend.
                # A successful defense occured.
                if len(self.players_in_attack()) == 0:
                    self.field_active = False
                # The defense continues.
                else:
                    self.field_active = True
                    self.attack_buffer += self.attacks
                    self.attacks *= 0
            elif move == _ACTION_GIVEUP:
                player.hand += self.attacks + self.attack_buffer + player.buffer
                self.field_active = False
            else: # The defense continues.
                for m in move:
                    current_buffer[m[0] // self.n_vals, m[0] % self.n_vals] = 1
                    self.field[m] = 1
                player.hand -= current_buffer
                player.buffer += current_buffer
                self.attack_buffer += self.attacks
                self.attacks *= 0

        elif player.is_wait():
            pass
        elif player.is_finished():
            pass

        # Note - even if there are cards remaining, an empty hand at end of round means you've finished play.
        if player.hand_is_empty():
            if player.is_defend():
                self.field_active = False
            player.finished()

    @staticmethod
    def _increment_move(move):
        """ Generator expression for incrementing moves """
        pass
