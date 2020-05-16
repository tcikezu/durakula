import numpy as np
from Agent import DurakPlayer
import Cards
from Cards import Deck

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
    """ Playing field for game of Durak.

    :param trump: the trump suit
    :type trump: int
    :param deck: the starting deck
    :type deck: Deck
    :param players: list of players
    :type players: list(DurakPlayer)
    """
    # Might be useful to convert this into **kwargs
    def __init__(self, trump, deck, players):

        self.numPlayers = len(players)
        self.players = players # list of Agent class objects
        self.cards = [player.hand.cards for player in players] # list of ndarrays
        self.trumpSuit = trump
        self.fieldDeck = deck
        self.garbage = Deck(mode=deck.mode)
        self.garbage.empty()
        self.bottomCard = None

        # self.trump = trump      # pretty sure we'll need the trump index later
        #
        # self.values_played = []
        #
        # self.battle_mask = CardCollection()
        # self.battle_mask[trump,:] = 1
        #
        # self.defense = CardCollection() # may be unnecessary
        # self.attack = CardCollection()
        # self.trash = CardCollection()

    def __str__(self):
        """ Output string for Field """

        head = '--- Playing Field ---\n'
        deck_str = 'Field Deck: \n' + str(self.fieldDeck) + '\n'
        player_list = [f'Player {i!r}:' + str(self.players[i].hand) +'\n' for i in range(self.numPlayers)]
        trump_str = 'Trump suit is ' + str(Cards._SUITS[self.trumpSuit]) + '\n'
        tail = '---------------------\n'
        return head + deck_str + ''.join(player_list) + trump_str + tail

    def get_legal_moves(self, player, attack, hand):
        # """ Returns all the legal moves, given if in attack or defense,
        # and given a hand.
        # Moves are CardCollections (4x13 arrays).
        # If legal, equals 1.
        # If illegal, equals 0.
        # """

        ## question :: are we okay with players getting sequential turns?

        if attack is True:
            valid_attacks = np.zeros((self.deck.n_suits, self.deck.n_vals)) # modify to be empty decks
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


    def list_moves(self, move_array, card_count = None):
        # """ create a list of possible moves (4,13), given the mask move_array and
        # # of cards per card value, card_count (1,13)
        #
        # if card_count is None, then we don't require a certain number of a card
        # value to be included in the list of moves"""
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
