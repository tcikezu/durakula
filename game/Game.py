import numpy as np
from random import choice
from collections import deque
from Field import DurakField
from Cards import Deck
from Agent import DurakPlayer

class Game:
    """
    Abstract class for card game play.
    """

    def __init__(self):
        pass

    def getinit_field(self):
        """
        Returns:
            init_field: a representation of the field (ideally this is the form
            that will be the input to your neural network)
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

    def getActionSize(self, player):
        """
        Returns:
            actionSize: number of all possible actions
        """
        pass

    def getNextState(self, action, player):
        """
        Input:
            players: current players who can make actions
            action: action taken by current players

        Returns
            nextField: field after applying action
            nextPlayer: player(s) who play(s) in the next turn
        """
        pass

    def getValidMoves(self, player):
        """
        Input:
            players: current player(s)

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
            moves that are valid from the current board and player, 0 for
            invalid moves
        """
        pass

    def getGameEnded(self, player):
        """
        Input:
            players: current players

        Returns:
            r: 0 if game has not ended. 1 if there is only one player remaining
            (who has lost)
        """
        pass

    # def stringRepresentation(self):
    #     """
    #     Returns:
    #         fieldString: a quick conversion of the field to a string format.
    #         Required by MCTS for hashing.
    #     """
    #     return self.__str__()

class DurakGame(Game):
    """ State machine for game of Durak.

    Args:
        n_players (int): The number of players playing a game of Durak.

        deckMode (str): This is either `full' or `small`.

    Attributes:
        n_players (int): The number of players playing a game of Durak.
        deck (Deck): The deck we're playing with
        players (list): A list of :class:`Agent.DurakPlayer` objects.
        playing_field (Field.DurakField): The playing field which contains rules for game-play.
        trump_suit (string): The selected trump suit.
        trump_idx (int): index for selected trump suit.
    """
    def __init__(self, n_players: int, deckMode: str) -> None:
        self.n_players = n_players
        self.deck = Deck(mode=deckMode)
        self.players = []
        self.playing_field = None
        self.init_field = None
        self.trump_suit = None
        self.trump_idx = None

        # Unsure if we want to begin game upon game construction.
        # Maybe we want to call this externally.
        self.beginGame()

    def getHandFromDeck(self, deck: Deck) -> np.ndarray:
        """ Convert a deck into a "hand", which is a 2d np.ndarray
        whose first row is always trump suit.

        Input:
            deck (Deck): The deck from which we get our hand
        """
        indices = list(range(deck.n_suits))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        return deck.cards[indices]

    def getDeckFromHand(self, hand: np.ndarray) -> Deck:
        """ Convert a hand into a deck object.

        Input:
            hand (np.ndarray): The hand whose first row corresponds to trump suit
        """
        indices = list(range(hand.shape[0]))
        indices[0], indices[self.trump_idx] = indices[self.trump_idx], indices[0]
        if hand.size == 52:
            deck = Deck(mode='full')
        elif hand.size == 36:
            deck = Deck(mode='small')
        else:
            raise ValueError('INVALID HAND SIZE')
        deck.empty()
        deck.cards = hand[indices]
        deck.order = deque([i for i, v in np.ndenumerate(deck.cards) if v == 1])
        return deck

    def beginGame(self):
        # Shuffle the deck.
        self.deck.shuffle()

        # Set trump idx
        self.trump_idx = self.deck.order[-1][0]
        self.trump_suit = self.deck.suit(-1)

        # Initialize the players.
        for i in range(self.n_players):
            hand = self.getHandFromDeck(self.deck.drawCard(6))
            self.players += [DurakPlayer(hand)]

        # Initialize the Field
        self.playing_field = DurakField(self.deck, self.players)
        self.init_field = self.playing_field

    def getInitfield(self):
        """ Initial Field """
        return self.init_field

    def getActionSize(self, playerID):
        """ available actions given player

        Args:
            playerID (int): index for player
        """
        return len(self.Field.get_legal_moves(playerID))

    def getGameEnded(self):
        """ Will return True when game is over. """
        return sum([len(player.deck) == 0 for player in self.players]) == self.n_players - 1
