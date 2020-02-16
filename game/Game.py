import Field


class Game(Field):
    """
    Abstract class for multi-agent, semi-turn-based games. In a
    semi-turn-based play, play begins with a player 1 committing action towards
    player 2. 2 can then respond. Depending on 2's response, play may then open
    to allow players 1, 3, ..., N to respond back.

    Basically, in this form of turn-based game, player "1" may increase to
    include all other players. So the one addition this Game class has to
    normal turn-based Game classes, is a method "addPlayers", which increases
    the number of players in self.player1.

    Use 1 for player 1, -1 for player 2, and 0 for all non-participating
    players.

    Something I don't fully understand is why they didn't just inherit from
    board?

    """

    def __init__(self):
        super().__init__()
        pass

    def get_init_field(self):
        """
        Returns:
            startField: a representation of the field (ideally this is the form
            that will be the input to your neural network)
        """
        pass def getFieldSize(self):
        """
        Returns:
            Originally returns (x,y): a tuple of dimensions
            Now: returns number of cards on the field? 
            Or maybe we can return number of `active' cards
        """
        pass

    def getActionSize(self):
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

    # I'm pretty sure this canonical form isn't something we need
    # def getCanonicalForm(self, field, *players):
        """
        Input:
            player: current player (1, 2, ..., N)

        Returns:
            canonicalField: returns canonical form of field. The canonical form
            should be independent of player. For e.g., in chess, field would be
            a board, and the canonical form can be chosen to be from the pov of
            white. When teh player is white, we can return board as is. When
            the player is black, we can invert the colors and return the
            board.
        """
    #    pass

    # def getSymmetries(self, field, pi):
        """
        Input:
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(field, pi)] where each tuple is a
            symmetrical form of the field and the corresponding pi vector. This
            is used when training the neural network from examples.
        """
    #    pass

    def stringRepresentation(self):
        """
        Returns:
            fieldString: a quick conversion of the field to a string format.
            Required by MCTS for hashing.
        """
        return self.__str__()
