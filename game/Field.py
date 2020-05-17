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
    """ Maintains deck in middle of table, and each player's deck.

    :param trump: the trump suit
    :type trump: int
    :param deck: the starting deck
    :type deck: Deck
    :param players: list of players
    :type players: list(DurakPlayer)
    """
    # Might be useful to convert this into **kwargs
    def __init__(self, deck, players):
        self.n_vals = deck.n_vals
        self.n_suits = deck.n_suits
        self.numPlayers = len(players)
        self.players = players # list of Agent class objects
        self.drawingDeck = deck
        self.garbage = Deck(mode=deck.mode).empty()
        # self.bottomCard = self.drawingDeck[-1]
        self.trumpSuit = self.drawingDeck.suit(-1)
        self.trumpSuitIdx = deck.order[-1][0]

        self.playerDurakHands = np.array([p.hand.ravel() for p in self.players])

        # field is a N x N array, where N = number of cards
        # columns are attacks
        # rows are defends
        # the first row of attacks and defends is always the trump suit
        # the first 13 rows and 13 columns of field also correspond to trump suit
        self.field = np.zeros((deck.cards.size, deck.cards.size))
        self.attacks = np.zeros_like(deck.cards)
        self.defends = np.zeros_like(deck.cards)

        self.playerOnDefense = np.random.randint(self.numPlayers)
        self.players[self.playerOnDefense].defend()
        self.playersOnAttack = [(self.playerOnDefense - 1) % self.numPlayers]
        self.players[self.playersOnAttack[0]].attack()

        # self.battle_mask = CardCollection()
        # self.battle_mask[trump,:] = 1

    def __str__(self):
        """ Output string for Field """

        head = '--- Playing Field ---\n'
        drawingdeck_str = 'Drawing Deck: ' + str(self.drawingDeck) + '\n'
        player_list = [f'Player {i!r}:' + str(self.players[i].hand) +'\n' for i in range(self.numPlayers)]
        trump_str = 'Trump suit is ' + self.trumpSuit + '\n'
        tail = '---------------------\n'
        return head + drawingdeck_str + ''.join(player_list) + trump_str + tail

    def get_legal_moves(self, playerID):
        if self.players[playerID].mode == 'defend':
            # Assuming there are attacks in self.attacks
            attack_idxs = np.flatnonzero(self.attacks) # use flatnonzero or argwhere
            trump_attack_idxs = [i for i,v in enumerate(attack_idxs) if v < self.n_vals]
            valid_defenses = np.zeros_like(self.field)
            f = lambda x : ceil(x / self.n_vals)*self.n_vals

            for att_idx in trump_attack_idxs:
                valid_defenses[att_idx + 1 : f(att_idx), att_idx] = 1
            for att_idx in attack_idxs:
                valid_defenses[att_idx + 1 : f(att_idx), att_idx] = 1
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
        else:
            raise ValueError('INVALID PLAYER MODE: MUST BE ONE OF "attack", "defend", "waiting"')

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
