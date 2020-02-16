class Field:
    def __init__(self):
        """
        See OthelloLogic.py for inspiration.

        Set up initial field configuration. The only buckets / sides to the
        field are those in attack, those in defense, those in neutral, and
        those who have finished playing.

        Therefore (in comparison to any boardgame) we don't need:
            - __getitem__

        """

    def __str__(self):
        """ to be returned by 'stringRepresentation' in game class """

        # Pseudocode:
        # All the cards on the field are (attack, defend) tuples
        # Want to join these into a string, while making sure we keep 
        # order of attack,defend pairs
        
        # (H6,H8)
        # (H8,S6)

        # etc

    def get_legal_moves(self):
        pass

    def has_legal_moves(self):
        pass

    def get_moves_for_card(self):
        pass

    def execute_move(self):
        pass

    @staticmethod
    def _increment_move(move):
        """ Generator expression for incrementing moves """
