import numpy as np
from Field import DurakField
from Cards import DurakDeck
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

class DurakHands:
    def __init__(self, deck, num_players):
        self.mode = deck.mode
        self.trump_idx = deck.trump_idx
        self.trump_suit = deck.trump_suit
        self.hands = np.zeros((num_players, deck.n_suits, deck.n_vals)).astype(int)

    def __getitem__(self, idx):
        return self.hands[idx]

    def __setitem__(self, idx, value):
        self.hands[idx] = value

    # def __eq__(self, other_hands):
    #     assert(self.hands.shape == other_hands.shape), "Oops! Hands shape mis-match."
    #     self.hands = other_hands

    def get_hand_from_deck(self, deck: DurakDeck, player_idx: int) -> None:
        """Create a hand to hands from an input deck.

        Args:
            deck (DurakDeck): A `DurakDeck` instance.
            player_idx (int): Player for whom we're creating the hand.
        """
        assert(deck.mode == self.mode), "Oops! Invalid deck mode!"
        indices = list(range(deck.n_suits))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        self.hands[player_idx] = deck.cards[indices]
        return self.hands[player_idx]

class DurakGame(Game):
    """State machine for game of Durak."""
    def __init__(self, n_players: int, deck_mode: str) -> None:
        # self.n_players = n_players
        self.players = []
        self.playing_field = None
        self.init_field = None
        self.hands = None

        # Unsure if we want to begin game upon game construction.
        # Maybe we want to call this externally.
        self.begin_game(n_players, deck_mode)

    def begin_game(self, n_players, deck_mode):
        """Deck is first shuffled, then 6 cards are dealt to each of the players. Finally the game's `Field` object is initialized."""
        # Create a deck object.
        deck = DurakDeck(mode=deck_mode)

        # Shuffle the deck.
        deck.shuffle()

        # Initialize the players and hands
        self.hands = DurakHands(deck, n_players)
        for player_id in range(n_players):
            self.hands.get_hand_from_deck(deck.draw_card(6), player_id)
            self.players += [DurakPlayer(self.hands[player_id], player_id, deck.trump_idx)]

        # Initialize the Field
        self.playing_field = DurakField(deck, self.hands, self.players)
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

    def get_game_ended(self):
        """Will return True when game is over."""
        return sum([player.player_mode == 'finished' for player in self.players]) == len(self.players) - 1

    def string_representation(self):
        """Print string representation of field."""
        return str(self.playing_field)
