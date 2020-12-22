import numpy as np
from copy import deepcopy
from rlcard.games.belote import Player
from rlcard.games.belote import Round
from rlcard.games.belote import Dealer

class BeloteGame(object):

    def __init__(self, allow_step_back=False):

        self.allow_step_back = allow_step_back
        self.num_players = 4
        # self.payoffs = [0 for _ in range(4)]
        self.np_random = np.random.default_rng()

    def init_game(self):
        ''' Initialize players and state
        Returns:
            (tuple): Tuple containing:
            (dict): The first state in one game
            (int): Current player's id
        '''
        # Initalize payoffs
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer
        self.dealer = Dealer(self.np_random)

        # Initialize four players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        # Deal cards to each player to prepare for the game
        self.dealer.deal_cards(self.players)

        # Initialize a Round
        self.round = Round(self.np_random)

        # Save the hisory for stepping back to the last state.
        self.history = []

        player_id = self.round.current_player
        actions = list(self.players[player_id].available_actions(self.round.public))
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):
        ''' Get the next state
        Args:
            action (str): A specific action
        Returns:
            (tuple): Tuple containing:
                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        ''' Return to the previous state of the game
        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_state(self, player_id):
        ''' Return player's state
        Args:
            player_id (int): player id
        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]
        public = self.round.public

        state = player.get_state(public, player.available_actions(public))
        return state

    def get_payoffs(self):
        ''' Return the payoffs of the game
        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        return self.round.payoffs

    def get_legal_actions(self):
        ''' Return the legal actions for current player
        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player)

    def get_player_num(self):
        ''' Return the number of players
        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    @staticmethod
    def get_action_num():
        ''' Return the number of applicable actions
        Returns:
            (int): The number of actions. There are 32 actions
        '''
        return 32

    def get_player_id(self):
        ''' Return the current player's id
        Returns:
            (int): current player's id
        '''
        return self.round.current_player

    def is_over(self):
        ''' Check if the game is over
        Returns:
            (boolean): True if the game is over
        '''
        return self.round.is_over

if __name__ == '__main__':
    # test init game
    game = BeloteGame()
    game.init_game()