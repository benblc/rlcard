from rlcard.games.belote.utils import get_available_actions

class BelotePlayer(object):
    ''' Player stores cards in the player's hand, and can determine the actions can be made according to the rules
    '''

    # player_id = None
    # hand = []

    def __init__(self, player_id, np_random):
        ''' Every player should have a unique player id
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.initial_hand = None
        self._current_hand = []
        self.stack = 0

    def current_hand(self):
        return self._current_hand

    def set_current_hand(self, value):
        self._current_hand = value

    def get_state(self, public, actions):  # TODO retravailler
        state = {}
        state['fold'] = public['fold']  # Cards list
        state['fold_starter'] = public['fold_starter']  # ID
        state['trace'] = public['trace'].copy()  # ??
        state['played_cards'] = public['played_cards'].copy()  # Cards list ?
        #         state['self'] = self.player_id
        #         state['initial_hand'] = self.initial_hand
        state['current_hand'] = self._current_hand  # Cards list
        #         state['others_hand'] = others_hands
        state['actions'] = actions  # ??
        state['card_holding'] = public['card_holding']  # Card
        state['player_holding'] = public['player_holding']  # ID
        state['fold_color'] = public['fold_color']  # Str
        state['player_id'] = self.player_id  # ID
        #         state['turn'] = public['turn']

        return state

    def available_actions(self, public):  # TODO comprendre mieux à quoi ça sert ??
        ''' Get the actions can be made based on the rules
        Args:

        Returns:
            list: list of string of actions. Eg: ['8S', '9H', 'TC', 'JD']
        '''

        return get_available_actions(self._current_hand, self.player_id, public)

    def play(self, action, greater_player=None):  # TODO ??
        ''' Perfrom action
        Args:
            action (string): specific action
            greater_player (Player object): The player who played current biggest cards.
        Returns:
            object of Player: If there is a new greater_player, return it, if not, return None
        '''
        raise NotImplementedError

        removed_cards = []
        self.played_cards = action
        for play_card in action:
            if play_card in trans:
                play_card = trans[play_card]
            for _, remain_card in enumerate(self._current_hand):
                if remain_card.rank != '':
                    remain_card = remain_card.rank
                else:
                    remain_card = remain_card.suit
                if play_card == remain_card:
                    removed_cards.append(self.current_hand[_])
                    self._current_hand.remove(self._current_hand[_])
                    break
            self._recorded_played_cards.append(removed_cards)
            return self

    def play_back(self):  ## TODO regarder où c'est utilisé quand c'est appeler??
        ''' Restore recorded cards back to self._current_hand
        '''
        raise NotImplementedError
        removed_cards = self._recorded_played_cards.pop()
        self._current_hand.extend(removed_cards)
        self._current_hand.sort(key=functools.cmp_to_key(sort_card))