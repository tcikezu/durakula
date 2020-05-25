from collections import deque, defaultdict
import numpy as np
from random import choice, shuffle
from Field import DurakField, _ACTION_GIVEUP
from Cards import DurakDeck

class Game:
    """
    Abstract class for card game play.
    """

    def __init__(self):
        pass

    def get_init_field(self):
        """
        Returns:
            init_field: a representation of the field (ideally this is the form that will be the input to your neural network)
        """
        pass

    # def getFieldSize(self):
    #     """
    #     Returns:
    #         Originally returns (x,y): a tuple of dimensions
    #         Now: returns number of cards on the field?
    #         Or maybe we can return number of `active' cards
    #     """
    #     pass

    def get_action_size(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        pass

    def get_next_state(self, board, action, player):
        """
        Input:
            players: current players who can make actions
            action: action taken by current players

        Returns
            nextField: field after applying action
            nextPlayer: player(s) who play(s) in the next turn
        """
        pass

    def get_valid_moves(self, board, player):
        """
        Input:
            players: current player(s)

        Returns:
            validMoves: a binary vector of length self.get_action_size(), 1 for moves that are valid from the current board and player, 0 for invalid moves
        """
        pass

    def get_game_ended(self, board, player):
        """
        Input:
            players: current players

        Returns:
            r: 0 if game has not ended. 1 if there is only one player remaining (who has lost)
        """
        pass

    def string_representation(self):
        """
        Returns:
            field_string: a quick conversion of the field to a string format.
            Required by MCTS for hashing.
        """
        pass

class MultiPlayerGame(Game):
    """Base class for multi-agent play."""
    def __init__(self):
        super().__init__()
        self.player = defaultdict()

    def new_player(self, player):
        pass

    def get_player(self, player):
        pass

_FINISHED = -2
_WAIT = -1
_ATTACK = 0
_DEFEND = 1
class DurakPlayers():
    """Wrapper class for managing the players in a game of Durak."""
    def __init__(self, n_suits, n_vals, n_players):
        self.player_states = np.zeros((3*n_players + 1, n_suits, n_vals))
        self.modes = self.player_states[:n_players]
        self.hands = self.player_states[n_players:2*n_players]
        self.buffers = self.player_states[2*n_players:]
        self.current_player = self.player_states[-1,0,0]

    def get_str(self, trump_idx):
        """Note - player numbering begins from 1, but the actual indices still begin from 0."""
        player_strs = [str(i+1) + ':' + str(DurakDeck.convert_hand_to_deck(hand, trump_idx)) for hand in self.hands]
        return '\n'.join(player_strs)

    def get_len(self, player = None):
        if player is None:
            return np.sum(self.hands[self.current_player])
        return np.sum(self.hands[player])

    def clear_buffer(self, player = None):
        """Remove all cards from the buffer hand."""
        if player is None:
            return self.buffers[self.current_player]
        self.buffers[player] *= 0

    def wait(self, player = None):
        if player is None:
            self.modes[self.current_player] *= 0
            self.modes[self.current_player] += _WAIT
        else:
            self.modes[player] *= 0
            self.modes[player] += _WAIT

    def attack(self, player = None):
        if player is None:
            self.modes[self.current_player] *= 0
            self.modes[self.current_player] += _ATTACK
        else:
            self.modes[player] *= 0
            self.modes[player] += _ATTACK

    def defend(self, player = None):
        if player is None
            self.modes[self.current_player] *= 0
            self.modes[self.current_player] += _DEFEND
        else:
            self.modes[player] *= 0
            self.modes[player] += _DEFEND

    def finished(self, player = None):
        if player is None:
            self.modes[self.current_player] *= 0
            self.modes[self.current_player] += _FINISHED
        else:
            self.modes[self.current_player] *= 0
            self.modes[self.current_player] += _FINISHED

    def is_wait(self, player = None) -> bool:
        if player is None:
            return self.modes[self.current_player].any() == _WAIT
        return self.modes[player].any() == _WAIT

    def is_attack(self, player = None) -> bool:
        if player is None
            return self.modes[self.current_player].any() == _ATTACK
        return self.modes[player].any() == _ATTACK

    def is_defend(self, player = None) -> bool:
        if player is None
            return self.modes[self.current_player].any() == _DEFEND
        return self.modes[player].any() == _DEFEND

    def is_finished(self, player = None) -> bool:
        if player is None:
            return self.modes[self.current_player].any() == _FINISHED
        return self.modes[player].any() == _FINISHED

    def hand_is_empty(self, player = None) -> bool:
        if player is None
            return np.sum(self.hands[self.current_player]) == 0
        return np.sum(self.hands[player]) == 0

    def set_current_player(self, player = None):
        """Set the active player id."""
        self.player_states[-1] *= 0
        self.player_states[-1] += player

    def get_defender(self):
        """Returns the player that is currently in defense mode."""
        return [p for p in range(self.n_players) if self.is_defend(p)][0]

    def get_attackers(self):
        """Returns a list of players that are attacking."""
        return [p for p in range(self.n_players) if self.is_attack(p)]

class DurakGame(Game):
    """State machine for game of Durak, a card game for 2-5 players."""
    def __init__(self, deck_mode, n_players) -> None:
        deck = DurakDeck(mode = deck_mode)
        self.players = DurakPlayers(deck.n_suits, deck.n_vals, n_players)

        self.n_players = n_players

        self.init_field = None
        self._begin_game(deck)

    def get_current_player(self):
        return self.players.current_player

    def _begin_game(self, deck):
        """Assume all players are now assigned player via self.new_player. Deck is shuffled, then cut. 6 cards are dealt to each of the players. Finally the playing field (`Field`) is initialized."""
        # Create a deck object.

        # Shuffle and cut the deck.
        shuffle(deck)
        deck.cut()
        trump_idx = deck[-1].suit_idx

        # Initialize player hands.
        for i in range(self.n_players):
            self.players.hands[i]= deck.draw_hand_from_deck(trump_idx=trump_idx, n_cards=6)

        # Decide who gets to attack and defend.
        highest_trump_cards = [(id, np.max(np.argwhere(hand[0,:]))) for id, hand in self.hands]
        shuffle(highest_trump_cards)
        first_player = min(highest_trump_cards, key=lambda x: x[1])[0]
        self.players.attack(first_player)
        self.players.defend((first_player + 1) % self.n_players)

        # Initialize the Field
        self.init_field = DurakField(deck, self.players, first_player)

    def get_init_field(self):
        """Initial Field"""
        return self.init_field

    def get_action_size(self, field, player):
        """Available actions given player

        Args:
            player (int): index for player
        """
        return len(field.get_legal_moves(player))

    def get_valid_moves(self, field, player=None):
        if player is None:
            return field.get_legal_moves(self.players.current_player)

    def _next_player(self, player: int) -> int:
        """By convention, the next valid player to the player's left."""
        for i in range(1, self.n_players):
            p = (player + i) % self.n_players
            if self.players.is_finished(p) == False:
                return p
        return None

    def _previous_player(self, player: int) -> int:
        """By convention, the next valid player to the player's right."""
        for i in range(1, self.n_players):
            p = (player - i) % self.n_players
            if self.players.is_finished(p) == False:
                return p
        return None

    def get_next_state(self, field: DurakField, player: int, action):
        """Updates the state of the playing field (`Field.DurakField`) after the player performs the given action. Resets the playing field if defense is successful or failed. Draws cards for players that have less than six cards while deck (`Cards.DurakDeck`) is unempty.

        Args:
            field (DurakField) : Current state of the field.
            player (int): Index of player
            action (tuple) or (str): Action player will take.

        Returns:
            field (DurakField): The field after applying action.
            player (int): The id of the next player who plays in the next turn.
        """

        # Immutable containers for storing defender and attackers before move is executed.
        initial_defender = self.players.get_defender()
        initial_attackers = tuple([p for p in self.players.get_attackers()])

        # Perform the action for given player and field, if player is either in defense or attack.
        # Otherwise, do nothing and move onto next available player.
        self.players.set_current_player(player)
        if self.players.is_attack() or self.players.is_defend():
            field.execute_move(action, player)
        if self.players.is_wait() or self.players.is_finished():
            next_player = self._next_player(player)
            self.players.set_current_player(next_player)
            return field, next_player

        if self.get_game_ended() != 0: # If game has ended, will return a player (value 1 - 5)
            return field, None

        # The playing field inactivates only after a successful or unsuccessful defense.
        if field.is_active == False:

            if len(action) == 0: # A successful defense happened.
                if self.players.is_finished():
                    new_defender = self._next_player(player)
                    new_attacker = self._previous_player(next_player)
                else: # Current player becomes new attacker.
                    new_attacker = player
                    new_defender = self._next_player(new_attacker)

            elif action == _ACTION_GIVEUP: # An unsuccessful defense happened.
                new_attacker = self._next_player(player)
                new_defender = self._next_player(new_attacker)

            assert(new_attacker != new_defender), "Attack and Defend are same player!"

            ###################### NEW ROUND BEGINS --- DRAW CARDS ########################
            # Retrieve attackers
            attackers = np.unique(field.attack_order, return_index = True)[1]

            # Obtain players attacked in order of attack
            unique_attack_order = [field.attack_order[i] for i in sorted(attackers)]

            # Draw from deck, first by order of attack, and lastly by defend.
            deck = field.deck
            for p in unique_attack_order + [initial_defender]:

                # Draw either enough cards to have 6 cards, or no cards.
                if self.players.is_finished(p) == False:
                    if len(deck) > 0:
                        self.players.hands[p] += DurakDeck.draw_hand_from_deck(deck.draw(max(6 - self.players.get_len(p),0)))
            field.clear_field()
            self.players.attack(new_attacker)
            self.players.defend(new_defender)
            self.players.set_current_player(new_attacker)
            return field, new_attacker
        else: # Field is still active. 
            if self.players.is_defend():
                if field.first_attack: # Attack passing only happens on first attack.
                    # Pass logic -- if a player plays the same value(s) of those of the first attack, then the attack is passed to next player. Note -- we do not need to ensure field wasn't empty, because field is active AND it was the first attack.
                    if len(np.unique(np.argwhere(field.attack_buffer + field.defense_buffer)[:,1])) == 1: # if attack was passed.
                        if self.players.is_finished() == False:
                            self.players.attack()

                        # New field state where next available defender is attacked with passed attack.
                        field.attacks += field.defense_buffer + field.attack_buffer
                        field.attack_buffer *= 0
                        field.defense_buffer *= 0
                        self.players.buffers[player] *= 0

                        new_defender = self._next_player(player)
                        self.players.defend(new_defender)

                        # New defender is next player to move.
                        self.players.set_current_player(new_defender)
                        return field, new_defender

                    else: # Attack isn't passed.
                        # Enable all waiting to attack.
                        for p in range(self.n_players):
                            if self.players.is_wait(p):
                                self.players.attack(p)

                        # As this is the first attack, we can choose amongst attack ids that weren't from the original attack.
                        attackers = [p for p in range(self.n_players) if self.players.is_attack(p) and p != initial_attackers[0]]
                        # However if this is none, then just add the original attacker. 
                        if attackers is None:
                            attackers = initial_attackers
                        new_attacker = choice(attackers)

                        # No longer in first attack.
                        field.set_first_attack(False)

                        # An attack is next.
                        self.players.set_current_player(new_attacker)
                        return field, new_attacker

                # If it is not the first attack, then we choose the next attacking player randomly.
                else:
                    # Here we don't need to enable anyone that is waiting to attack, since it's no longer the first attack.
                    random_player = choice(initial_attackers)
                    self.players.set_current_player(random_player)
                    return field, random_player

            # If player was attacking, then next player has to be the defender.
            if self.players.is_attack():
                # Chose to do nothing.
                if len(action) == 0:
                    self.players.wait()

                    # Choose a new attacker.
                    attackers = [p for p in range(self.n_players) if self.players.is_attack(p) and p != player]
                    if len(attackers) > 0:
                        next_player = choice(attackers)
                    else:
                        next_player = initial_defender
                # Chose to attack:
                else:
                    next_player = initial_defender
                self.players.set_current_player(next_player)
                return field, next_player
        if self.players.is_wait():
            raise ValueError('Attempted an action with waiting player.')
        if self.players.is_finished():
            raise ValueError('Attempted an action with finished player.')

    def get_game_ended(self):
        """Will return 0 if game has not ended, or the player, counting from 1 through 5, of the loser of the game."""
        if sum([self.players.modes[p] == 'finished' for p in range(self.n_players)]) == self.n_players - 1:
            return np.argwhere(self.players.modes == _FINISHED)[0][0]
        else:
            return 0

    def string_representation(self):
        """Print string representation of field."""
        return str(field)
