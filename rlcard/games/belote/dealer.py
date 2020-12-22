
import functools

from rlcard.games.belote.utils import init_32_deck
from rlcard.games.belote.utils import cards2str, sort_card

class BeloteDealer(object):
    ''' Initialize a belote dealer class
    '''

    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_32_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal some cards from deck to one player
        Args:
            player (object): object of BelotePlayer
            num (int): The number of cards to be dealed
        '''
        for index, player in enumerate(players):
            current_hand = self.deck[index * 8:(index + 1) * 8]
            current_hand.sort(key=functools.cmp_to_key(sort_card))
            # player.set_current_hand(current_hand)
            player._current_hand = current_hand
            player.initial_hand = cards2str(current_hand)