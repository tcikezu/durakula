from Card import Card

class Deck:
    def __init__(self, mode='full'): 
        self.mode = None
        self.deck = []
        self.set_mode(mode)
        self.get_cards()

    def __str__(self):
        card_names = []
        for c in self.deck:
            card_names.append(c.__str__())
        return ' '.join(card_names)
        
    def __len__(self):
        return len(self.deck)

    def set_mode(self, mode):
        assert mode in set(['full', 'small'])
        self.mode = mode

    def build_deck(self, suits, values):
        for s in suits:
            for v in values:
                self.deck.append(Card(s,v))

    def get_cards(self):    
        if self.mode == 'full':
            suits = ['S', 'C', 'H', 'D']
            values = range(2,15)
 
        elif self.mode == 'small':
            suits = ['S', 'C', 'H', 'D']
            values = range(6,15)
 
        else:
            raise Exception('Invalid Deck Type.')
        self.build_deck(suits, values)

