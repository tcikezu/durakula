import Numpy as np 
from pytorch_classification.utils import Bar, AverageMeter
import time
import Game


class Arena(Game):
    """
    An Arena class where any number of agents can be pit against each other.
    """

    def __init__(self, pDefend, *pAttack):
        """
        Input:
            Players: A list of player functions, each of which takes board
            as input, and returns action

            I'm considering making each player, a callable Class (ie, a
            function with a property like 'attacking'.)
        """
        super().__init__()

        # Still unsure as to how we should set variables here. 
        self.pDefend = pDefend
        self.pAttack = pAttack
        self.N = len(pAttack) + 1

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player 1, ..., N if
                player N)
            or
                draw result returned from the game that is neither (1 ... N)
        """

    def playGames(self, num, verbose=False):
        """
        Plays num games, where player starts an equal number of games
        (ie num / self.N)

        Returns:
            a win-vector counting # of games won, indexed by player
            (assume there are no draws)
        """

        eps_time = AverageMeter()
        bar = Bar('Arena.playGames', max=num)
        end = time.time()
        eps = 0
        maxeps = int(num)

        # write two for loops here that correspond to num / self.N plays of a
        # game, iterating over player start. 

        return wins
