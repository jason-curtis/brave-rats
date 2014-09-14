from enum import Enum


class Card(Enum):
    musician = 0
    princess = 1
    spy = 2
    assassin = 3
    ambassador = 4
    wizard = 5
    general = 6
    prince = 7

    @classmethod
    def get_from_int(cls, n):
        return (
            item for item in cls if item.value is n
        ).next()


def initial_hand(hand_str=None):
    if hand_str:
        return [Card.get_from_int(int(x)) for x in hand_str]
    else:
        # In a vanilla game, players will start with one of each card
        return [card for card in Card]

Color = Enum('Color', 'red blue')
