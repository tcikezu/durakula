from utils import *
from Field import DurakField, _ACTION_GIVEUP
from Cards import DurakDeck, DurakHand
from Agent import DurakPlayer

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

    def get_action_size(self, player):
        """
        Returns:
            actionSize: number of all possible actions
        """
        pass

    def get_next_state(self, action, player):
        """
        Input:
            players: current players who can make actions
            action: action taken by current players

        Returns
            nextField: field after applying action
            nextPlayer: player(s) who play(s) in the next turn
        """
        pass

    def get_valid_moves(self, player):
        """
        Input:
            players: current player(s)

        Returns:
            validMoves: a binary vector of length self.get_action_size(), 1 for moves that are valid from the current board and player, 0 for invalid moves
        """
        pass

    def get_game_ended(self, player):
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

class DurakGame(Game):
    """State machine for game of Durak."""
    def __init__(self, n_players: int, deck_mode: str, dealer = False) -> None:
        # self.n_players = n_players
        self.players = []
        self.playing_field = None
        self.init_field = None
        self.n_players = n_players

        # At some point I want to make an additional player called `dealer' that gets to select the index at which they cut the deck and shuffle however they want `

        # Unsure if we want to begin game upon game construction.
        # Maybe we want to call this externally.
        self.begin_game(deck_mode)

    def begin_game(self, deck_mode):
        """Deck is shuffled, then cut. 6 cards are dealt to each of the players. Finally the playing field (`Field`) is initialized."""
        # Create a deck object.
        deck = DurakDeck(mode=deck_mode)

        # Shuffle and cut the deck.
        shuffle(deck)
        deck.cut()

        # Initialize the players and hands
        for player_id in range(self.n_players):
            self.players += [DurakPlayer(deck, player_id)]

        # Decide who gets to attack and defend.
        weakest_players = [(id, np.argmax(p.hand[0,:])) for id, p in enumerate(self.players)]
        shuffle(weakest_players)
        first_player_id = min(weakest_players, key=lambda x: x[1])[0]
        self.players[first_player_id].attack()
        self.players[(first_player_id + 1) % self.n_players].defend()

        # Initialize the Field
        self.playing_field = DurakField(deck, self.players)
        self.init_field = self.playing_field

    def get_init_field(self):
        """Initial Field"""
        return self.init_field

    def get_action_size(self, player_id):
        """Available actions given player

        Args:
            player_id (int): index for player
        """
        return len(self.Field.get_legal_moves(player_id))

    def get_valid_moves(self, player_id):
        return self.playing_field.get_legal_moves(player_id)

    def _next_player(self, player_id: int) -> int:
        """By convention, the next valid player to the player's left."""
        for i in range(1, self.n_players):
            p = self.players[(player_id + i) % self.n_players]
            if p.is_finished() == False:
                return p.player_id

    def _previous_player(self, player_id: int) -> int:
        """By convention, the next valid player to the player's right."""
        for i in range(1, self.n_players):
            p = self.players[(player_id - i) % self.n_players]
            if p.is_finished() == False:
                return p.player_id

    def get_next_state(self, action, player_id):
        """Updates the state of the playing field (`Field.DurakField`) after player (`Agent.DurakPlayer`) performs the given action. Resets the playing field if defense is successful or failed. Draws cards for players that have less than six cards while deck (`Cards.DurakDeck`) is unempty.

        Args:
            action (tuple) or (str): Action player will take.
            player_id (int): Index of player

        Returns:
            new_field (Field.DurakField): The field after applying action.
            next_player_id (int): The id of player who plays in the next turn.
        """

        # Immutable containers for defend and attack player ids.
        # Moving this before execute_move because it's possible that on first attack, the attacker runs out of cards, and initial_attack_ids is empty.
        initial_defend_id = self.playing_field.player_in_defense().player_id
        initial_attack_ids = tuple([p.player_id for p in self.playing_field.players_in_attack()])

        player = self.players[player_id]
        self.field.set_active_player(player_id)
        if player.is_attack() or player.is_defend():
            self.playing_field.execute_move(action, player_id)
        if player.is_wait() or player.is_finished():
            next_player_id = self._next_player(player_id) 
            self.playing_field.set_active_player(next_player_id)
            return self.playing_field, next_player_id

        # The playing field is only inactivated after a defending player successfully defends, or fails to defend. Thus the below case only happens if the current player is defending. This also means the next player id is new_attack_id.
        if self.playing_field.field_active == False:
            assert(player.is_defend()), f'Expected defend, instead got !{player.player_mode}'

            # A successful defense happened.
            if len(action) == 0:
                if player.is_finished():
                    new_defend_id = self._next_player(player_id)
                    new_attack_id = self._previous_player(next_player)
                else:
                    new_attack_id = player_id
                    new_defend_id = self._next_player(new_attack_id)

            # Defense was unsuccessful.
            elif action == _ACTION_GIVEUP:
                new_attack_id = self._next_player(player_id)
                new_defend_id = self._next_player(new_attack_id)

            assert(new_attack_id != new_defend_id), "Attack and Defend are same player!"

            # Retrieve indices of those who attacked
            attack_indices = np.unique(self.playing_field.attack_order, return_index = True)[1]

            # Obtain player ids of those that attacked, in order of attack
            unique_attack_order = [self.playing_field.attack_order[i] for i in sorted(attack_indices)]

            # Draw from deck, first by order of attack, and lastly by defend.
            deck = self.playing_field.drawing_deck
            for id in unique_attack_order + [initial_defend_id]:

                # Draw either enough cards to have 6 cards, or no cards.
                if self.players[id].is_finished() == False:
                    if len(deck) > 0:
                        self.players[id].get_hand_from_deck(deck.draw_card(max(6 - len(self.players[id]),0)))
                # Is it possible for there to not be enough cards in the deck? Ie is it possible that after we draw cards, one person doesn't get to draw any cards, so they've finished? I think the game is structured so that that should never be the case.

            # Reset the field.
            self.playing_field.clear_field()
            self.players[new_attack_id].attack()
            self.players[new_defend_id].defend()
            self.playing_field.set_active_player(new_attack_id)
            return self.playing_field, new_attack_id
        else:
            # Field is still active. If player was defending, then it's another player's turn to attack, unless player passed along the attack. If player was attacking, then it's the defender's turn to defend.
            if player.is_defend():

                # See if attack is passed along to next player:
                if self.playing_field.first_attack:
                    attack_passed = False

                    # Pass logic -- if a player plays the same value(s) of those of the first attack, then the attack is passed to next player. All pass does is move defend position. Note -- we do not need to ensure field wasn't empty, because field is active AND it was the first attack.
                    if len(np.unique(np.argwhere(self.playing_field.attack_buffer + self.playing_field.defense_buffer)[:,1])) == 1: # if pass is true
                        if player.is_finished() == False:
                            player.attack() # Then player is now attacking or finished.
                            self.playing_field.attacks += player.buffer + self.playing_field.attack_buffer
                            self.playing_field.attack_buffer *= 0
                            player.buffer *= 0
                            attack_passed = True


                        # Pass the attack.
                        print('passed')
                        new_defend_id = self._next_player(player_id)
                        self.players[new_defend_id].defend()

                        # Enable all waiting to attack.
                        for p in self.players:
                            if p.is_wait():
                                p.attack()

                        # No longer in first attack.
                        self.playing_field.set_first_attack(attack_passed)

                        # New defender is next player to move.
                        self.playing_field.set_active_player(new_defend_id)
                        return self.playing_field, new_defend_id

                    # The attack is not passed onto the next player.
                    else:
                        # Enable all waiting to attack.
                        for p in self.players:
                            if p.is_wait():
                                p.attack()

                        # As this is the first attack, we can choose amongst attack ids that weren't from the original attack.
                        attack_ids = [p.player_id for p in self.players if p.is_attack() and p.player_id != initial_attack_ids[0]]
                        new_attack_id = choice(attack_ids)

                        # No longer in first attack.
                        self.playing_field.set_first_attack(False)

                        # An attack is next.
                        self.playing_field.set_active_player(new_attack_id)
                        return self.playing_field, new_attack_id

                # If it is not the first attack, then we choose the next attacking player randomly.
                else:
                    # Here we don't need to enable anyone that is waiting to attack, since it's no longer the first attack.
                    random_player_id = choice(initial_attack_ids)
                    self.playing_field.set_active_player(random_player_id)
                    return self.playing_field, random_player_id

            # If player was attacking, then next player has to be the defender.
            if player.is_attack():
                # Chose to do nothing.
                if len(action) == 0:
                    player.wait()

                    # Choose a new attacker.
                    attack_ids = [p.player_id for p in self.players if p.is_attack() and p.player_id != player_id]
                    if len(attack_ids) > 0:
                        next_player_id = choice(attack_ids)
                    else:
                        next_player_id = initial_defend_id
                # Chose to attack:
                else:
                    next_player_id = initial_defend_id
                self.playing_field.set_active_player(next_player_id)
                return self.playing_field, next_player_id
        if player.is_wait():
            raise ValueError('Attempted an action with waiting player.')
        if player.is_finished():
            raise ValueError('Attempted an action with finished player.')

    def get_game_ended(self):
        """Will return True when game is over."""
        return sum([player.player_mode == 'finished' for player in self.players]) == len(self.players) - 1

    def string_representation(self):
        """Print string representation of field."""
        return str(self.playing_field)
