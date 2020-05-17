import numpy as np
from Agent import DurakPlayer
import Cards
from Cards import Deck
import copy
from itertools import combinations
from math import ceil

class Field:
    """Abstract field class. Create rules of the field here."""
    def __init__(self):
    	pass
    def __str__(self):
    	pass
    def get_legal_moves(self):
    	pass
    def list_moves(self):
    	pass
    def has_legal_moves(self):
    	pass
    def execute_move(self):
    	pass

    # @staticmethod
    # def _increment_move(move):
    # 	""" Generator expression for incrementing moves """

class DurakField(Field):
    """ This class defines legal moves you can make in a game of Durak, given
    every players' hands and the current cards played on the field. 

    Input:
        deck (Deck): A deck that is optionally the deck from which we draw all values.

        players (list): A list of :class:`Agent.DurakPlayer` objects

    Attributes:
        field (np.ndarray): The 'table' in N x N form, where N is the total number of cards
    in the initial deck. The columns correspond to attacks, and rows correspond to
    defends, for each attack.


    """
    # Might be useful to convert this into **kwargs
    def __init__(self, deck, players):
        self.n_vals = deck.n_vals
        self.n_suits = deck.n_suits
        self.n_players = len(players)
        self.players = players # list of Agent class objects
        self.trump_suit = self.drawing_deck.suit(-1)
        self.trump_suit_idx = deck.order[-1][0]

        self.player_durak_hands = np.array([p.hand.ravel() for p in self.players])

        # field is a N x N array, where N = number of cards
        # columns are attacks
        # rows are defends
        # the first row of attacks and defends is always the trump suit
        # the first 13 rows and 13 columns of field also correspond to trump suit
        self.field = np.zeros((deck.cards.size, deck.cards.size))
        self.buffer = np.zeros((deck.cards.size, deck.cards.size))
        self.attacks = np.zeros_like(deck.cards)
        self.defends = np.zeros_like(deck.cards)

        self.player_on_defense = np.random.randint(self.n_players)
        self.players[self.player_on_defense].defend()
        self.players_on_attack = [(self.player_on_defense - 1) % self.n_players]
        self.players[self.players_on_attack[0]].attack()

        # self.battle_mask = CardCollection()
        # self.battle_mask[trump,:] = 1

    def __str__(self):
        """ Output string for Field """

        head = '--- Playing Field ---\n'
        drawing_deck_str = 'Drawing Deck: ' + str(self.drawing_deck) + '\n'
        player_list = [f'Player {i!r}:' + str(self.players[i].hand) +'\n' for i in range(self.n_players)]
        trump_str = 'Trump suit is ' + self.trump_suit + '\n'
        tail = '---------------------\n'
        return head + drawing_deck_str + ''.join(player_list) + trump_str + tail

    def get_legal_moves(self, playerID):
        if self.players[playerID].mode == 'defend':
            # Assuming there are attacks in self.attacks
            attack_idxs = np.flatnonzero(self.attacks) # use flatnonzero or argwhere
            nontrump_attack_idxs = attack_idxs[attack_idxs >= self.n_vals]
            valid_defenses = np.zeros_like(self.field)
            f = lambda x : (x // self.n_vals + 1)*self.n_vals

            for att_idx in attack_idxs:
                valid_defenses[att_idx + 1 : f(att_idx), att_idx] = 1
            for att_idx in nontrump_attack_idxs:
                valid_defenses[:self.n_vals, att_idx] = 1

            valid_defenses *= self.players[playerID].hand.ravel()[:,np.newaxis]
            return valid_defenses # + ['pass']

        elif self.players[playerID].mode == 'attack':
            # print('attack mode')
            # Assuming there cards on the field.
            valid_attacks = np.zeros_like(self.attacks)
            if np.sum(self.field).astype('int') > 0:
                attack_idxs = np.unique(np.argwhere(self.field)[:,1])
                valid_attacks[:,attack_idxs] = 1
                valid_attacks *= self.players[playerID].hand
            else:
                valid_attacks = self.players[playerID].hand

            return valid_attacks # + ['wait']

        elif mode == 'waiting':
            return ['wait', 'attack']
        elif mode == 'finished':
            return []
        else:
            raise ValueError('INVALID PLAYER MODE: MUST BE ONE OF "attack", "defend", "waiting", "finished"')

    def list_moves(self, valid_moves):
        pass

    def has_legal_moves(self, attack):
        if attack is True:
            return sum(get_legal_moves(self, attack)) > 0
        else: return

    def execute_move(self, attack):
        if attack is True:
            pass
        else:
            pass

    @staticmethod
    def _increment_move(move):
        """ Generator expression for incrementing moves """
