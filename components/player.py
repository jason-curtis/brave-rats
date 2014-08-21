from components import cards


class CheatingException(Exception):
    pass


class Player(object):
    def __init__(self, color, brain_fn):
        '''
        :param color: a Color enum value indicating which color this player is playing for
        :param game: a GameStatus object
        :param brain_fn: The brains of the operation. See example_ai.py for an example.
            Should be a function which takes two required inputs:
            player: a Player instance used for accessing the player's hand
            game: a GameStatus instance for accessing game details
             and one optional input:
            spied_card: if player successfully played a spy the previous turn, this will be the card that the other
                player has revealed to play.
            Should return a card from its hand to play. Can harbor hidden powers; should be expected to be called
                exactly once per round.
        '''
        self.hand = cards.initial_hand()
        self.color = color
        self.card_choosing_fn = brain_fn

    def has_cards(self):
        return bool(len(self.hand))

    def choose_and_play_card(self, game, spied_card=None):
        card = self.card_choosing_fn(self, game, spied_card)
        if card not in self.hand:
            raise CheatingException('Tried to play card {} which is not in hand'.format(card))
        self.hand.remove(card)
        return card
