import numpy as np
from rlcard.envs import Env


class BeloteEnv(Env):
    ''' Belote Environment
    '''

    def __init__(self, config):
        from rlcard.games.belote.utils import CARD_TRAIT_STR
        from rlcard.games.belote.utils import ACTION_LIST, ACTION_SPACE
        from rlcard.games.belote.utils import encode_cards
        from rlcard.games.belote.utils import cards2str
        from rlcard.games.belote import Game

        self._encode_cards = encode_cards
        self._cards2str = cards2str
        self._CARD_TRAIT_STR = CARD_TRAIT_STR
        self._ACTION_LIST = ACTION_LIST
        self._ACTION_SPACE = ACTION_SPACE

        self.name = 'belote'
        self.game = Game()
        super().__init__(config)
        self.state_shape = [4, 33]

    def _extract_state(self, state):
        ''' Encode state
        Args:
            state (dict): dict of original state
        Returns: TODO en parler à PE / y reflechir papier crayon
            numpy array: 4*33 array
                         the current fold with cards being one hot encoded + 1 coordinate for the player playing first
        '''
        obs = np.zeros(self.state_shape, dtype=int)
        self._encode_cards(obs, state['fold'], state['fold_starter'])

        extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions(state)}

        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            # TODO: state['actions'] can be None, may have bugs
            if state['actions'] == None:
                extracted_state['raw_legal_actions'] = []
            else:
                extracted_state['raw_legal_actions'] = [a for a in state['actions']]

        if self.record_action:
            extracted_state['action_record'] = self.action_recorder

        return extracted_state

    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.
        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        return self.game.get_payoffs()

    def _decode_action(self, action_id):
        ''' Action id -> the action in the game. Must be implemented in the child class.
        Args:
            action_id (int): the id of the action
        Returns:
            action (string): the action that will be passed to the game engine.
        '''

        return self._ACTION_LIST[action_id]

    def _get_legal_actions(self, state):  # TODO renvoie les ID des legal_action dans game.state['actions']
        ''' Get all legal actions for current state
        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_action_id = []
        legal_actions = state['actions']
        if legal_actions:
            for action in legal_actions:
                legal_action_id.append(self._ACTION_SPACE[action])
        return legal_action_id

    def get_perfect_information(self):  # TODO après avoir bien défini ce qu'est un bon state
        ''' Get the perfect information of the current state
        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['hand_cards'] = [self._cards2str(player._current_hand) for player in self.game.players]
        state['landlord'] = self.game.state['landlord']
        state['trace'] = self.game.state['trace']
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.state['actions']
        return state

