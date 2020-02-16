import numpy as np
import time

class Arena():
    """
    An Arena class where any numPlayers agents can be pit against each other.
    """

    def __init__(self, players, game, display=None):
        """
        Input:
            Players: A list of player functions, that takes board
            as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
            display in othello/Othello Game).

        """

        self.players = players # original script specifies individual players:
        # e.g. self.player1 = player1, self.player2 = player2
        self.N = len(players)
        self.game = game
        self.display = display

    def playGame(self, verbose = False):
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
        """

        eps_time = AverageMeter()
        bar = Bar('Arena.playGames', max=num)
        end = time.time()
        eps = 0
        maxeps = int(num)

        # write two for loops here that correspond to num / self.N plays of a
        # game, iterating over player start. 
        

        return wins
