import numpy as np
from Agent import DurakPlayer
import Cards
from Cards import Deck
import copy
from itertools import combinations

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
    """ Maintains deck in middle of table, and each player's hands.

    :param trump: the trump suit
    :type trump: int
    :param deck: the starting deck
    :type deck: Deck
    :param players: list of players
    :type players: list(DurakPlayer)
    """
    # Might be useful to convert this into **kwargs
    def __init__(self, deck, players):
        self.numPlayers = len(players)
        self.players = players # list of Agent class objects
        self.cards = [player.hand.cards for player in players] # list of ndarrays
        self.drawingDeck = deck
        self.fieldDeck = Deck(mode=deck.mode).empty()
        self.garbage = Deck(mode=deck.mode).empty()
        self.bottomCard = self.drawingDeck[-1]
        self.trumpSuit = self.drawingDeck.suit(-1)

        self.attackDeck = Deck(mode=deck.mode).empty()
        self.defenseDeck = Deck(mode=deck.mode).empty()

        # self.bottomCard = Deck(mode=deck.mode).empty()
        # self.bottomCard[self.drawingDeck.order[-1]] = 1 
        self.trumpSuitIdx = deck.order[-1][0]

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
        fielddeck_str = 'Field Deck: ' + str(self.fieldDeck) + '\n'
        player_list = [f'Player {i!r}:' + str(self.players[i].hand) +'\n' for i in range(self.numPlayers)]
        trump_str = 'Trump suit is ' + self.trumpSuit + '\n'
        tail = '---------------------\n'
        return head + drawingdeck_str + fielddeck_str + ''.join(player_list) + trump_str + tail

    def get_legal_moves(self, playerID):
        if playerID.mode == 'defend':
            valid_defends = Deck(mode=self.attackDeck.mode).empty()
            valid_defends.cards[self.trumpSuitIdx,:] = 1

            for idx in self.attackDeck.order:
                valid_defends.cards[idx[0],idx[1] + 1:] = 1
                valid_defends.cards[idx[0],:idx[1]] = 0
            
            valid_defends.cards *= self.players[playerID].hand.cards
            valid_defends.order.append([idx for idx, val in np.ndenumerate(valid_defends.cards) if val == 1])
            return list(valid_defends.order)
        
        elif playerID.mode == 'defend':
            valid_defenses = Deck(mode=self.fieldDeck.mode).empty() # modify to be empty decks

            # this for loop gives valid cards you can put down,
            # but it doesn't specify a number of cards that have
            # to be put down for the defense to be valid.
            for index in self.attack.nonzero():
                valid_defenses[index[0],index[1]+1:] = 1

            return list_moves(valid_defenses, np.sum(self.attack, axis=1))
        elif mode == 'waiting':
            return []
        else:
            return 'INVALID PLAYER MODE: MUST BE ONE OF "attack", "defend", "waiting"'

    #def list_moves(self, move_array, card_count = None):
    #    # """ create a list of possible moves (4,13), given the mask move_array and
    #    # # of cards per card value, card_count (1,13)
    #    #
    #    # if card_count is None, then we don't require a certain number of a card
    #    # value to be included in the list of moves"""
    #    all_moves = []
    #    if card_count is None:
    #        move_list = np.argwhere(move_list > 0)
    #        move_iterable = iter(move_list)
    #        for L in range(0, len(move_list)+1):
    #            for subset in combinations(move_list, L):
    #                all_moves.append(tuple(subset)) # Forms a list of tuples
    #    # Do later
    #    else:
    #        move_list = move_array.nonzero()

    #    return all_moves

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
