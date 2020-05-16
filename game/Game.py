import numpy as np
from random import choice
from Field import DurakField
from Cards import Deck
from Agent import DurakPlayer

class Game:
    """
    Abstract class for card game play.
    """

    def __init__(self):
        pass

    def getInitField(self):
        """
        Returns:
            initField: a representation of the field (ideally this is the form
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
    """ Implement state machine for game of Durak. Note, the agents here are
    called players since we haven't implemented AI Agents (yet).
    """
    def __init__(self, numPlayers: int, deckMode: str) -> None:
        self.numPlayers = numPlayers
        self.deck = Deck(mode=deckMode)
        self.players = []
        self.playingField = None
        self.initField = None

        # Unsure if we want to begin game upon game construction.
        # Maybe we want to call this externally.
        self.beginGame()

    def beginGame(self):
        # Initialize the players
        for i in range(self.numPlayers):
            self.players += [DurakPlayer(self.deck)]

        # Initialize the players' hands.
        for id in range(self.numPlayers*6):
            self.players[id % self.numPlayers].drawHand(self.deck, 1)

        # Choose a trump suit
        trumpSuit = choice(range(self.deck.n_suits))

        # Initialize the Field
        self.playingField = DurakField(trumpSuit, self.deck, self.players)
        self.initField = self.playingField

    def getInitField(self):
        """ Initial Field """
        return self.initField

    def getActionSize(self, playerID):
        """ available actions given player

        :param playerID: input player
        :type playerID: int
        """
        return len(self.Field.get_legal_moves(playerID))
