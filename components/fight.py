from enum import Enum
from components.cards import Card, Color


FightResult = Enum('FightResult', 'red_wins red_wins_2 blue_wins blue_wins_2 on_hold red_wins_game blue_wins_game')


def _short_format_result(fight_result_):
    ''' returns a one- to two-character representation of a FightResult
    '''
    return {
        FightResult.red_wins: 'r',
        FightResult.blue_wins: 'b',
        FightResult.red_wins_2: 'r2',
        FightResult.blue_wins_2: 'b2',
        FightResult.on_hold: 'h'
    }[fight_result_]


def fight_result(red_card, blue_card, prev_red_card, prev_blue_card):
    ''' The main game engine. Figures out what the result of played cards should be.
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
        return FightResult.red_wins_game
    if blue_has_power and blue_card == Card.princess and red_card == Card.prince:
        return FightResult.blue_wins_game

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


def print_results_table(red_general_played=False):
    ''' Prints a results table similar to that provided with the Brave Rats card game.
    :param red_general_played: if True,
    :return: None; output is printed to stdout
    '''
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


def resolve_fight(red_card, blue_card, game):
    ''' Given a fight, updates the game state according to the resolution of that fight
    :param red_card: Card enum value played by red player
    :param blue_card: Card enum value played by blue player
    :param game: GameStatus instance to be updated
    '''
    previous_red_card, previous_blue_card = game.most_recent_fight
    print 'red:', red_card.name, 'vs. blue:', blue_card.name
    result = fight_result(red_card, blue_card, previous_red_card, previous_blue_card)
    print 'result:', result.name

    if result == FightResult.on_hold:
        game.on_hold_fights.append((red_card, blue_card))
    else:
        game.resolved_fights.extend(game.on_hold_fights)
        game.resolved_fights.append((red_card, blue_card))
        points_from_on_hold = game.on_hold_points
        game.on_hold_fights = []

    if result in [FightResult.red_wins, FightResult.red_wins_2]:
        extra_point = 1 if result is FightResult.red_wins_2 else 0
        game.red_points += 1 + points_from_on_hold + extra_point

    if result in [FightResult.blue_wins, FightResult.blue_wins_2]:
        extra_point = 1 if result is FightResult.blue_wins_2 else 0
        game.blue_points += 1 + points_from_on_hold + extra_point

    # If you win by princess, just max out the scoreboard
    if result == FightResult.red_wins_game:
        game.red_points = 999999
    if result == FightResult.blue_wins_game:
        game.blue_points = 999999


def successful_spy_color((red_card, blue_card)):
    ''' Determine whether the provided fight has a non-nullified spy in it
    Takes a fight tuple of (red_card, blue_card)
    :return: Color of non-nullified spy, if any, or None if no non-nullified spy.
    '''
    spy_nullifiers = {Card.musician, Card.wizard, Card.spy}
    if red_card == Card.spy and blue_card not in spy_nullifiers:
        return Color.red
    if blue_card == Card.spy and red_card not in spy_nullifiers:
        return Color.blue
    return None
