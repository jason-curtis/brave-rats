import random

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


Color = Enum('Color', 'red blue')


FightResult = Enum('FightResult', 'red_wins red_wins_2 blue_wins blue_wins_2 on_hold')


def _short_format_result(fight_result):
    ''' returns a one- to two-character representation of a FightResult
    '''
    return {
        FightResult.red_wins: 'r',
        FightResult.blue_wins: 'b',
        FightResult.red_wins_2: 'r2',
        FightResult.blue_wins_2: 'b2',
        FightResult.on_hold: 'h'
    }[fight_result]


def fight_result(red_card, blue_card, prev_red_card, prev_blue_card):
    ''' The brains of the operation. Figures out what the result of played cards should be.
    :return: a FightResult
    '''
    #5. Wizard - nullifies opponent's power
    blue_has_power = red_card != Card.wizard
    red_has_power = blue_card != Card.wizard

    #0. Musician - round is put on hold
    if red_has_power and red_card == Card.musician:
        return FightResult.on_hold
    if blue_has_power and blue_card == Card.musician:
        return FightResult.on_hold

    #1. Princess - wins against prince
    if red_has_power and red_card == Card.princess and blue_card == Card.prince:
        return FightResult.red_wins
    if blue_has_power and blue_card == Card.princess and red_card == Card.prince:
        return FightResult.blue_wins

    #7. Prince - you win the round
    if red_has_power and red_card == Card.prince and blue_card != Card.prince:
        return FightResult.red_wins
    if blue_has_power and blue_card == Card.prince and red_card != Card.prince:
        return FightResult.blue_wins

    #6. General - next round, your card gets +2 strength
    if prev_red_card == Card.general and prev_blue_card not in [Card.wizard, Card.musician]:
        red_value = red_card.value + 2
    else:
        red_value = red_card.value
    if prev_blue_card == Card.general and prev_red_card not in [Card.wizard, Card.musician]:
        blue_value = blue_card.value + 2
    else:
        blue_value = blue_card.value

    #3. Assassin - Lowest strength wins
    modifier = -1 if (red_has_power and red_card == Card.assassin)\
                  or (blue_has_power and blue_card == Card.assassin) else 1

    if modifier * red_value > modifier * blue_value:
        #4. Ambassador - win with this counts as 2 victories
        if red_has_power and red_card == Card.ambassador:
            return FightResult.red_wins_2
        return FightResult.red_wins
    elif modifier * red_value < modifier * blue_value:
        #4. Ambassador - win with this counts as 2 victories
        if blue_has_power and blue_card == Card.ambassador:
            return FightResult.blue_wins_2
        return FightResult.blue_wins
    else:
        return FightResult.on_hold


def _random_witty_remark(card):
    return random.choice([
        'A {card} is a good choice.',
        'Really? A {card}?',
        '{card} is my favorite.',
        '{card} goes to battle!',
        'Hmm. {card}...',
        'okeydokey',
        'Good luck, {card}!',
        'nice knowing ya, {card}',
    ]).format(card=card.name)


def _input_card(color, valid_cards):
    ''' Prompts CLI user to enter a card, with retries on validation failure.
    '''

    try:
        card_number = input('{} card #: '.format(color.name.title()))
    except (SyntaxError, NameError):
        print 'Just a number please'
        return _input_card(color, valid_cards)

    try:
        card = Card.get_from_int(int(card_number))
    except (NameError, StopIteration):
        print card_number, 'is not a card number. Try again.'
        return _input_card(color, valid_cards)
    else:
        if card in valid_cards:
            print _random_witty_remark(card)
            return card
        else:
            print 'Nice try! You already played your', card.value
            return _input_card(color, valid_cards)


def input_fight():
    '''
    A simple manual-input one-on-one card fight for testing purposes
    '''
    red_card = _input_card(Color.red, Color)
    blue_card = _input_card(Color.blue, Color)

    print 'Result:', fight_result(red_card, blue_card, None, None)


class Player(object):
    def __init__(self, color):
        self.hand = [card for card in Card]
        self.color = color

    def has_cards(self):
        return bool(len(self.hand))

    def choose_card(self):
        raise NotImplementedError

    def choose_and_play_card(self):
        card = self.choose_card()
        self.hand.remove(card)
        return card


class RandomAIPlayer(Player):
    def choose_card(self):
        return random.choice(self.hand)


class HumanPlayer(Player):
    def choose_card(self):
        return _input_card(self.color, self.hand)


def game_vs_ai():
    print 'You are playing against the computer!!! be afeared!'
    red_player = HumanPlayer(Color.red)
    blue_player = RandomAIPlayer(Color.blue)

    red_points, blue_points = 0, 0

    on_hold_points = 0
    previous_red_card, previous_blue_card = None, None
    while red_points < 4 and blue_points < 4 and red_player.has_cards():
        red_card, blue_card = red_player.choose_and_play_card(), blue_player.choose_and_play_card()
        print 'red:', red_card.name, 'vs. blue:', blue_card.name
        result = fight_result(red_card, blue_card, previous_red_card, previous_blue_card)
        print 'result:', result.name

        if result in [FightResult.red_wins, FightResult.red_wins_2]:
            extra_point = 1 if result is FightResult.red_wins_2 else 0
            red_points += 1 + on_hold_points + extra_point
            on_hold_points = 0
        elif result in [FightResult.blue_wins, FightResult.blue_wins_2]:
            extra_point = 1 if result is FightResult.blue_wins_2 else 0
            blue_points += 1 + on_hold_points + extra_point
            on_hold_points = 0
        else:
            on_hold_points += 1

        print 'red has', red_points, 'to blue\'s', blue_points, 'with', on_hold_points, 'rounds on hold'
        previous_red_card, previous_blue_card = red_card, blue_card
    if red_points >= 4:
        print 'red wins!'
        return
    if blue_points >= 4:
        print 'blue wins!'
        return
    else:
        print 'tie!'
        return


def print_results_table(red_general_played=False):
    format_cell = '{}'.format
    previous_red = Card.general if red_general_played else None

    # Table header
    print ' ', '\t', '\t'.join('b=' + format_cell(card.value) for card in Card)

    for red_card in Card:
        print '\t'.join(
            ['r=' + format_cell(red_card.value)] +  # Row header
            [
                format_cell(_short_format_result(fight_result(red_card, blue_card, previous_red, None)))
                for blue_card in Card
            ]
        )


if __name__ == '__main__':
    while True:
        game_vs_ai()
