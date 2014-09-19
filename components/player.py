from components import cards
from components.brain_management import unprefixed_name


class CheatingException(Exception):
    pass


class Player(object):
    def __init__(self, color, brain_fn, hand_str=None):
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
        :param hand_str: string of card values in initial hand (eg. '0123456' to play without Prince)
        '''
        self.hand = cards.initial_hand(hand_str)
        self.color = color
        self.card_choosing_fn = brain_fn

    def has_cards(self):
        return bool(len(self.hand))

    def choose_and_play_card(self, game, spied_card=None):
        card = self.card_choosing_fn(self, game, spied_card)
        if card not in self.hand:
            raise CheatingException(
                '{} tried to play card {} which is not in hand {}'
                .format(unprefixed_name(self.card_choosing_fn), card, self.hand)
            )
        self.hand.remove(card)
        return card

    def notify_game_over(self, game):
        # Call the brain function and give it a chance to clean up now that the game's over
        self.card_choosing_fn(self, game, None)
