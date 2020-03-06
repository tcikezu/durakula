from Cards import *
import numpy as np
from itertools import combinations

class Field:
    def __init__(self, trump, num_players):
        """
        Set up initial field configuration.

        Attributes:
        """
        self.num_players = num_players
        self.deck = Deck(mode='full')
        self.hands = np.array([self.deck.draw(n=6) for player in range(num_players)])
        self.trump = trump      # pretty sure we'll need the trump index later

        self.values_played = []
        
        self.battle_mask = CardCollection()
        self.battle_mask[trump,:] = 1

        self.defense = CardCollection() # may be unnecessary
        self.attack = CardCollection()
        self.trash = CardCollection()

    def __str__():
        pass

    def to_string(self):
        """ to be returned by 'stringRepresentation' in game class """

        # Pseudocode:
        # All the cards on the field are (attack, defend) tuples
        # Want to join these into a string, while making sure we keep 
        # order of attack,defend pairs
        
        # (H6,H8)
        # (H8,S6)


    def get_legal_moves(self, attack, hand):
        """ Returns all the legal moves, given if in attack or defense,
        and given a hand.
        Moves are CardCollections (4x13 arrays).
        If legal, equals 1.
        If illegal, equals 0.
        """

        ## question :: are we okay with players getting sequential turns?

        if attack is True:
            valid_attacks = np.zeros((4,13)) # modify to be empty decks
            valid_attacks[:,self.values_played] = 1
            valid_attacks *= hand

            return list_moves(valid_attacks)


            # DEPRECATED:
            # below doesn't quite work if we want to reset the defense field
            # after executing attack
            # valid_attacks = np.zeros((4,13))
            # valid_attacks[:,np.sum(self.defense,axis=0) > 0] = 1
            # valid_attacks *= hand
            # return valid_attacks.nonzero()
        else:
            valid_defenses = np.zeros((4,13)) # modify to be empty decks
            
            # this for loop gives valid cards you can put down, 
            # but it doesn't specify a number of cards that have
            # to be put down for the defense to be valid. 
            for index in self.attack.nonzero():
                valid_defenses[index[0],index[1]+1:] = 1

            # valid defenses now looks like [[0, 0, 1, 1, 1, 1, ...], [0,
            # ...0], ...], if attack was at [0,1], for example.
            
            return list_moves(valid_defenses, np.sum(self.attack, axis=1))
            

    def list_moves(move_array, card_count = None):
        """ create a list of possible moves (4,13), given the mask move_array and 
        # of cards per card value, card_count (1,13)

        if card_count is None, then we don't require a certain number of a card
        value to be included in the list of moves"""
        all_moves = []
        if card_count is None:
            move_list = np.argwhere(move_list > 0)
            move_iterable = iter(move_list)
            for L in range(0, len(move_list)+1):
                for subset in combinations(move_list, L):
                    all_moves.append(tuple(subset)) # Forms a list of tuples
        # Do later
        else:
            move_list = move_array.nonzero()
            
        return all_moves

    def has_legal_moves(self, attack):
        if attack is True:
            return sum(get_legal_moves(self, attack)) > 0
        else:
            return 

    def execute_move(self, attack):
        if attack is True:
            pass
        else:
            pass

    @staticmethod
    def _increment_move(move):
        """ Generator expression for incrementing moves """
