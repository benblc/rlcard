class Card(object):
    '''
    Card stores the color and trait of a single card
    Note:
        The color variable in a standard card game should be one of [S, H, D, C, BJ, RJ] meaning [Spades, Hearts, Diamonds, Clubs, Black Joker, Red Joker]
        Similarly the trait variable should be one of [A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K]
    '''

    color = None
    trait = None
    valid_color = ['S', 'H', 'D', 'C', 'BJ', 'RJ']
    valid_trait = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    def __init__(self, color, trait):
        ''' Initialize the color and trait of a card
        Args:
            color: string, color of the card, should be one of valid_color
            trait: string, trait of the card, should be one of valid_trait
        '''
        self.color = color
        self.trait = trait

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.trait == other.trait and self.color == other.color
        else:
            # don't attempt to compare against unrelated types
            return NotImplemented

    def __hash__(self):
        color_index = Card.valid_color.index(self.color)
        trait_index = Card.valid_trait.index(self.trait)
        return trait_index + 100 * color_index

    def __str__(self):
        ''' Get string representation of a card.
        Returns:
            string: the combination of trait and color of a card. Eg: AS, 5H, JD, 3C, ...
        '''
        return self.trait + self.color

    def get_index(self):
        ''' Get index of a card.
        Returns:
            string: the combination of color and trait of a card. Eg: 1S, 2H, AD, BJ, RJ...
        '''
        return self.color+self.trait