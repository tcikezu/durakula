class NeuralNet():
    """
    This class specifies the base NeuralNet class. To define our own neural
    network, we need to subclass this clas and implement the below functions.
    The neural network does not consider the current player, and instead only
    deals with the `canonical' form of the board / field.

    See othello/NNet.py for an example implementation.
    """

    def __init__(self, game):
        pass

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            exapmles: a list of training examples, where each example is of
            from (field, pi, v). pi is the MCTS informed policy vector for the
            given field, and v is its value. The examples has field in its
            canonical form.

        """
        pass
 
    def predict(self, field):
        """
        Input:
            field: current field in its canonical form.

        Returns:
            pi: a policy vector for the current field- a numpy array of length
            game.getActionSize

            v: a float in [-1,1] that gives the value of the current board
        """
        pass

    def save_checkpoint(self, folder, filename):
        """
        Saves the current neural network (with its parameters) in folder /
        filename
        """
        pass

    def load_checkpoint(self, folder, filename):
        """
        loads parameters of the neural network from folder / filename
        """
        pass
