import numpy as np 
from pytorch_classification.utils import Bar, AverageMeter
import time

class Arena:
    """This class's methods and comments are taken from Shantanu Thakoor (see ShantanuThakoor/alpha-zero-general) @ github"""
    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that take board as input, return action
            game: Game object
            display: a function that takes board as input and prints it
        pass
        """
        pass
    def play_game(self, verbose=False):
        """
        Executes one episode of a game.
        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        pass
    def play_games(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player 2 starts num/2 games.
        Returns
            oneWon: games won by player1
            twoWon: games won by player2
            draws: games won by nobody
        """
        pass

class DurakArena(Arena):
    """
    An Arena class that manages player actions taking place in a given game.
    Originally designed for card games where players have to be given cards
    at the start of the game.
    """

    def __init__(self, game, *players, display=None):
        """
        Input:
            Players: A list of player functions, each of which takes board
            as input, and returns an action.
            game: Game object
            display: a function that takes Board as input and prints it out.
        """

        self.player_functions = [player for player in players]
        self.n_players = len(self.player_functions)
        self.game = game
        self.display = display

    def play_game(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player 1, ..., N if
                player N)
            or
                draw result returned from the game that is neither (1 ... N)
        """
        current_player = self.game.get_current_player()
        field = self.game.get_init_field()
        it = 0
        while self.game.get_game_ended(field, current_player) == 0:
            it += 1
            if verbose:
                assert self.display
                print("turn ", str(it), "Player ", str(current_player))
                self.display(field)
            action = self.player_functions[current_player](field, current_player)
            valids = self.game.get_valid_moves(field, current_player)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debut(f'valids = {valids}')
                assert valids[action] > 0
            field, current_player = self.game.get_next_state(field, current_player, action)
        if verbose:
            assert self.display
            print("Game over: Turn ", str(it), "Result ", str(self.game.get_game_ended()), " lost.")
        return game.get_game_ended()

    def play_games(self, num, verbose=False):
        """
        Plays num games, where player starts an equal number of games
        (ie num / self.N)

        Returns:
            a loss-vector counting # of games lost, indexed by player
            (assume there are no draws)
        """

        # eps_time = AverageMeter()
        # bar = Bar('Arena.playGames', max=num)
        # end = time.time()
        # eps = 0
        # maxeps = int(num)

        # write two for loops here that correspond to num / self.N plays of a
        # game, iterating over player start. 

        num = int(num / self.n_players)
        n_lost = np.zeros(self.n_players)
       
        for _ in tqdm(range(num), desc=f'Arena.playGames'):
            game_result = self.play_game(verbose=verbose)
            n_lost[game_result] += 1

        return n_lost
