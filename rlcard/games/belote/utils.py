# Utils

from rlcard.games.belote.card import Card

# a map of trait to its index
TRAIT_MAP = {'7': 0, '8': 1, '9': 2, 'J': 3, 'Q': 4,
             'K': 5, 'T': 6, 'A': 7}

TRAIT_MAP_ATOUT = {'7': 0, '8': 1, 'Q': 2, 'K': 3,
                   'T': 4, 'A': 5, '9': 6, 'J': 7}

POINTS_DIC = {'7S': 0, '7D': 0, '7C': 0, '8S': 0, '8D': 0, '8C': 0, '9S': 0, '9D': 0, '9C': 0, 'JS': 2, 'JD': 2,
              'JC': 2, 'QS': 3, 'QD': 3, 'QC': 3, 'KS': 4, 'KD': 4, 'KC': 4, 'TS': 10, 'TD': 10, 'TC': 10, 'AS': 11,
              'AD': 11, 'AC': 11, '7H': 0, '8H': 0, 'QH': 3, 'KH': 4, 'TH': 10, 'AH': 11, '9H': 14, 'JH': 20}

CARD_TRAIT_STR = [key for key in POINTS_DIC.keys()]

ACTION_SPACE = {}
for index, key in enumerate(POINTS_DIC):
    ACTION_SPACE[key] = index

ACTION_LIST = list(ACTION_SPACE.keys())


def init_32_deck():
    ''' Initialize a standard deck of 32 cards
    Returns:
        (list): A list of Card object
    '''
    color_list = ['S', 'H', 'D', 'C']
    trait_list = ['A', '7', '8', '9', 'T', 'J', 'Q', 'K']
    res = [Card(color, trait) for color in color_list for trait in trait_list]
    return res


def sort_card(card_1, card_2):
    ''' Compare the trait of two cards of Card object
    Args:
        card_1 (object): object of Card
        card_2 (object): object of card
    '''

    CARD_trait = ['7', '8', '9', 'J', 'Q', 'K', 'T', 'A']
    CARD_trait_A = ['7', '8', 'Q', 'K', 'T', 'A', '9', 'J']

    key = []
    for card in [card_1, card_2]:
        if card.color == 'H':
            key.append(CARD_trait_A.index(card.trait))
        else:
            key.append(CARD_trait.index(card.trait))
    if (card_1.color == 'H') & (card_2.color == 'H'):
        if key[0] > key[1]:
            return 1
        elif key[0] < key[1]:
            return -1
        else:
            return 0
    elif (card_1.color != 'H') & (card_2.color != 'H'):
        if key[0] > key[1]:
            return 1
        elif key[0] < key[1]:
            return -1
        else:
            return 0
    elif (card_1.color == 'H') & (card_2.color != 'H'):
        return 1

    elif (card_1.color != 'H') & (card_2.color == 'H'):
        return -1


def cards2str(cards):
    res = ''
    for card in cards:
        res += str(card)
    return res


def hand2dict(hand):
    ''' Get the corresponding dict representation of hand
    Args:
        hand (list): list of string of hand's card
    Returns:
        (dict): dict of hand with best card for atout
    '''
    hand_dict = {'S': 0, 'H': 0, 'D': 0, 'C': 0,
                 'best_H': '7'}

    for card in hand:
        hand_dict[card.color] += 1
        if card.color == 'H':
            if TRAIT_MAP_ATOUT[card.trait] >= TRAIT_MAP_ATOUT[hand_dict['best_H']]:
                hand_dict['best_H'] = card.trait
    return hand_dict


def count_points(str_cards_list, turn):
    if turn == 8:
        res = 10
    else:
        res = 0
    if str_cards_list:
        for card in str_cards_list:
            res += POINTS_DIC[card]
    return res

def compute_final_payoffs(players):
    points_even = players[0].stack
    points_odd = players[1].stack
    winner = points_odd > points_even

    return winner, [160 * (1 - winner), 160 * winner, 160 * (1 - winner), 160 * winner]


def get_available_actions(hand, player_id, public):
    hand_dict = hand2dict(hand)
    fold_color = public['fold_color']
    card_holding = public['card_holding']
    player_holding = public['player_holding']

    legal_actions = []
    if fold_color:
        if hand_dict[fold_color] > 0:  # The player can play the asked color
            if fold_color != 'H':  # Asked color is not atout
                for card in hand:
                    if card.color == fold_color:
                        legal_actions.append(str(card))
            else:  # Asked color is atout
                if TRAIT_MAP_ATOUT[hand_dict['best_H']] > TRAIT_MAP_ATOUT[
                    card_holding.trait]:  # Player has a better atout than the best one played in the fold
                    for card in hand:
                        if (card.color == 'H') & (TRAIT_MAP_ATOUT[card.trait] > TRAIT_MAP_ATOUT[
                            card_holding.trait]):  # All atout better than the best one played are legals
                            legal_actions.append(str(card))
                else:  # Player does not have a better atout
                    for card in hand:
                        if card.color == 'H':  # All player's atout are legal
                            legal_actions.append(str(card))

        else:  # The player cannot play the asked color
            if fold_color == 'H':  # Asked color is atout
                for card in hand:  # The player can play any card
                    legal_actions.append(str(card))
            else:  # Asked color is not atout
                if hand_dict['H'] > 0:  # Player has some atout
                    if player_holding % 2 != player_id % 2:  # Opposing team is holding the fold
                        if card_holding.color == fold_color:  # No atout has been played in this fold
                            for card in hand:
                                if card.color == 'H':  # Only the player's atout are legal
                                    legal_actions.append(str(card))
                        else:  # Someone has already played an atout
                            if TRAIT_MAP_ATOUT[hand_dict['best_H']] > TRAIT_MAP_ATOUT[
                                card_holding.trait]:  # Player has a better atout than the best one played in the fold
                                for card in hand:
                                    if (card.color == 'H') & (TRAIT_MAP_ATOUT[card.trait] > TRAIT_MAP_ATOUT[
                                        card_holding.trait]):  # Only atout better than the best one played are legals
                                        legal_actions.append(str(card))
                            else:  # Player does not have a better atout
                                for card in hand:
                                    if card.color == 'H':  # All player's atout are legal
                                        legal_actions.append(str(card))
                    else:  # Player's ally is holding the fold
                        for card in hand:
                            legal_actions.append(str(card))  # All player's cards are legal
                else:  # Player does not have any atout
                    for card in hand:
                        legal_actions.append(str(card))  # All player's cards are legal
    else:
        for card in hand:
            legal_actions.append(str(card))
    return legal_actions


def compare_cards(card_1, card_2, fold_color):
    '''Returns:
        best card between card_1 and card_2 in fold'''
    if card_1.color == 'H':
        if card_2.color != 'H':
            return card_1
        elif TRAIT_MAP_ATOUT[card_1.trait] > TRAIT_MAP_ATOUT[card_2.trait]:
            return card_1
        else:
            return card_2

    elif card_1.color == fold_color:
        if card_2.color == 'H':
            return card_2
        elif card_2.color == fold_color:
            if TRAIT_MAP[card_1.trait] > TRAIT_MAP[card_2.trait]:
                return card_1
            else:
                return card_2
        else:
            return card_1
    else:
        return card_2


def get_best_card(card_list, fold_color):
    '''
    Args:
        card_list : a list of Cards objects forming a fold
        fold_color : the color of the first card played in the fold

    Returns :
        best card in the list given atout
    '''
    if not card_list:
        return None
    else:
        try:
            len(card_list)
        except TypeError:
            return card_list
        else:
            best_card = card_list[0]
            for card in card_list:
                best_card = compare_cards(card, best_card, fold_color)

        return best_card


def encode_cards(plane, cards, starting_player_id):
    ''' Encode cards and represerve it into plane.
    Args:
        plane (int) : plane to encode onto
        cards (list or str): list or str of cards
        starting_player_id (int) : the id of the player that started the fold
    '''
    if not cards:
        return None

    if len(cards) == 1:
        index = CARD_TRAIT_STR.index(str(cards[0]))
        plane[starting_player_id][index] = 1
        plane[starting_player_id][-1] = 1

    else:
        for id, card in enumerate(cards):
            index = CARD_TRAIT_STR.index(str(card))
            current_player_id = (starting_player_id + id) % 4
            plane[current_player_id][index] = 1
            if id == 0:
                plane[starting_player_id][-1] = 1

def decode_state_human(state):
    res = []
    obs = state['obs']
    for player_id in range(4):
        for card_num in range(32):
            if obs[player_id][card_num]:
                res.append((player_id,ACTION_LIST[card_num]))
    return res