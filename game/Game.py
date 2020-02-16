class Game:
    def __init__(self):
        pass

    def getInitField(self):
        """
        Returns:
            startField: a representation of the field (ideally this is the form
            that will be the input to your neural network)
        """
        pass

    # Have to check the implementation but I think we probably won't need board
    # size.

    def getFieldSize(self):
        """
        Returns:
            Originally returns (x,y): a tuple of dimensions
        """

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """

    def getNextState(self, field, action, player):
        """
        Input:
            field: current field
            player: current player (1, 2, ..., N)
            action: action taken by current player

        Returns
            nextField: field after applying action
            nextPlayer: player who plays in the next turn
        """
    
    def getValidMoves(self, field, *player):
        """
        Input:
            field: current field
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
            moves that are valid from the current board and player, 0 for
            invalid moves
        """
        
        pass

    def getGameEnded(self, field, *player):
        """
        Input:
            field: current field
            Player: current player (1 ... N)

        Returns:
            r: 0 if game has not ended. 1 if there is only one player remaining
            (who has lost)
        """

        pass

    # I'm pretty sure this canonical form isn't something we need
    def getCanonicalForm(self, field, *player):
        """
        Input:
            field: curernt field
            player: current player (1, 2, ..., N)

        Returns:
            canonicalField: returns canonical form of field. The canonical form
            should be independent of player. For e.g., in chess, field would be
            a board, and the canonical form can be chosen to be from the pov of
            white. When teh player is white, we can return board as is. When
            the player is black, we can invert the colors and return the
            board. 
        """

        pass

    def getSymmetries(self, field, pi):
        """
        Input:
            field: current field
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(field, pi)] where each tuple is a
            symmetrical form of the field and the corresponding pi vector. This
            is used when training the neural network from examples.
        """

    def stringRepresentation(self, field):
        """
        Input:
            field: current field

        Returns:
            fieldString: a quick conversion of the field to a string format.
            Required by MCTS for hashing.
        """
