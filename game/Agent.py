import numpy as np

class Player:
    """A player object is initialized with the game. Its main function is to take the state of the game (ie the board) as input, and return an action."""
    def __init__(self, game):
        pass

    def play(self, board):
        """Given the board, return an action."""
        pass

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, field):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

class HumanPlayer():
    def __init__(self, game):
        self.game = game

class MultiPlayer():
    """Base class for games involving more than 2 players."""
    def __init__(self, game):
        self.game = game
        self.game.new_player(self)

    def play(self, field):
        pass

def RandomMultiPlayer(MultiPlayer):
    def __init__(self, game):
        super().__init__(game)
    
    def play(self, field):
        a = np.random.randint(self.game.get_action_size())
        valids = self.game.get_valid_moves(field)
        while valids[a] != 1:
            a = np.random.randint(self.game.get_action_size())
        return a

def HumanDurakPlayer(MultiPlayer):
    def __init__(self, game):
        super().__init__(game)

    def play(self, field) -> None:
        action = None
        while(action is None):
            if self.game.players.is_defend():
                action = input("Select an action: 0 - defend, 1 - pass.")
            if self.game.players.is_attack():
                action = input("Select an action: 0 - attack, 1 - pass.")
            if action != 0 or action != 1:
                action = None
        if action == 0:
            valid_moves = [str(i) + ': ' + str(move) for i,move in enumerate(game.get_valid_moves())]
            print('Valid moves: ', ' '.join(valid_moves))
            move = None
            while(move is None):
                move = input('Choose a valid move:')
                if move < 0 or move >= len(valid_moves):
                    move = None
            return move
        elif action == 1:
            return

def GreedyMultiPlayer(MultiPlayer):
    def __init__(self, game):
        super().__init__(game)
    
    def play(self, field):
        pass

def MCTSMultiPlayer(MultiPlayer):
    def __init__(self, MCTS, game):
        super().__init__(game)
        self.mcts = MCTS

    def play(self, field):
        pass
