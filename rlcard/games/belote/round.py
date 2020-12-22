from rlcard.games.belote.utils import get_best_card
from rlcard.games.belote.utils import compute_final_payoffs
from rlcard.games.belote.utils import count_points
from rlcard.games.belote.utils import cards2str


class BeloteRound(object):

    def __init__(self, np_random):
        ''' Initialize the round class
        Args:
            dealer (object): the object of UnoDealer
            num_players (int): the number of players in game
        '''
        self.trace = []
        self.np_random = np_random
        self.card_holding = None
        self.player_holding = None
        self.current_player = 0
        self.fold = []
        self.fold_color = None
        self.fold_starter = 0
        self.turn = 1
        self.is_over = False
        self.winner = None
        self.atout = 'H'
        self.played_cards = []
        self.payoffs = [0 for _ in range(4)]
        self.public = {'card_holding': self.card_holding, 'player_holding': self.player_holding, 'played_cards': [],
                       'fold_color': self.fold_color, 'trace': self.trace, 'fold': self.fold, 'fold_starter': self.fold_starter}

    def update_public(self):
        ''' Updates public after update to round
        '''

        self.public['card_holding'] = self.card_holding
        self.public['player_holding'] = self.player_holding
        self.public['trace'] = self.trace
        self.public['played_cards'] = self.played_cards
        self.public['fold'] = self.fold
        self.public['fold_color'] = self.fold_color
        self.public['fold_starter'] = self.fold_starter


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running
        Args:
            players (object): object of BelotePlayer
            action (str): string of legal action
        '''

        self.trace.append((self.current_player, action))
        player = players[self.current_player]
        color = action[1]
        trait = action[0]

        remove_index = None

        for index, card in enumerate(player._current_hand):
            if color == card.color and trait == card.trait:
                remove_index = index
                break

        card = player._current_hand.pop(remove_index)

        self.fold.append(card)
        self.played_cards.append(str(card))

        if len(self.fold) == 1:  # First card of the fold is played
            self.fold_color = color
            self.card_holding = card
            self.player_holding = self.current_player
            self.fold_starter = self.current_player

        else:
            best_card = get_best_card(self.fold, self.fold_color)
            if self.card_holding != best_card:  # The card played is the new holding card
                self.card_holding = best_card  # Update card_holding
                self.player_holding = self.current_player  # Update team holding

        if len(self.fold) == 4:  # End of the current turn
            fold_winner = players[self.player_holding]
            fold_winner_ally = players[(self.player_holding+2)%4]
            fold_points = count_points([str(card) for card in self.fold], self.turn)
            fold_winner.stack += fold_points
            fold_winner_ally.stack += fold_points

            self.compute_payoffs(fold_points, fold_winner.player_id)
            self.fold_starter = fold_winner.player_id
            self.fold = []
            self.player_holding = None
            self.card_holding = None
            self.fold_color = None

            if self.turn == 8:
                self.is_over = True
                self.winner, self.payoffs = compute_final_payoffs(players)
            else:
                self.turn += 1
                self.current_player = fold_winner.player_id

        else:
            self.current_player = (self.current_player + 1) % 4

        self.update_public()

    def compute_payoffs(self, fold_points, fold_winner_id):
        if (fold_winner_id%2):
            self.payoffs = [0, fold_points, 0, fold_points]
        else:
            self.payoffs = [fold_points, 0, fold_points, 0]
