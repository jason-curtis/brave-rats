#!/usr/bin/python
#  -*- coding: UTF8 -*-
from collections import Counter
import sys
from brave_rats import play_match

from components.brain_management import discover_brains, unprefixed_name
from components.cards import Color
from components.style import redify, blueify, color_pad


EXCLUDED_BRAIN_NAMES = {'human'}


def _table_cell(contents):
    return u' {:22} |'.format(contents)


def _print_table_cell(contents):
    sys.stdout.write(_table_cell(contents))


def _print_table_row(contents):
    for item in contents:
        _print_table_cell(item)
    sys.stdout.write('\n')


def print_summary(results, all_ais):
    ai_names = [''] + [unprefixed_name(ai) for ai in all_ais]
    _print_table_row([blueify(name) for name in ai_names])
    for red_ai in all_ais:
        _print_table_cell(redify(unprefixed_name(red_ai)))
        for blue_ai in all_ais:
            try:
                games = results[(red_ai, blue_ai)]
            except KeyError:
                win_count = {Color.red: '-', Color.blue: '-', None: '-'}
            else:
                winners = [game.winner for game in games]
                win_count = Counter(winners)
            result_descrip = u'{}/{}/{}'.format(
                u'←{}'.format(win_count[Color.red]),
                win_count[None],
                u'↑{}'.format(win_count[Color.blue]),
            )
            if win_count[Color.red] > win_count[Color.blue]:
                colored_result_descrip = redify(result_descrip)
            elif win_count[Color.red] < win_count[Color.blue]:
                colored_result_descrip = blueify(result_descrip)
            else:
                colored_result_descrip = color_pad(result_descrip)
            _print_table_cell(colored_result_descrip)
        _print_table_row([])


def play_round_robin(num_games=1000):
    brains_dict = discover_brains()
    all_ais = [
        brain_fn
        for name, brain_fn in brains_dict.iteritems()
        if name not in EXCLUDED_BRAIN_NAMES
    ]
    ai_names = [unprefixed_name(ai) for ai in all_ais]

    print '{} AIs discovered:'.format(len(all_ais))
    print 'AIs:'
    print '\n'.join(ai_names)

    results = {}
    for red_ai in all_ais:
        for blue_ai in all_ais:
            raw_input(
                'Next match: {} vs. {}'.format(
                    redify(unprefixed_name(red_ai)),
                    blueify(unprefixed_name(blue_ai))
                )
            )
            games = list(play_match(red_ai, blue_ai, num_games=num_games, verbose=True, quiet_games=True))
            results[(red_ai, blue_ai)] = games
            print_summary(results, all_ais)

if __name__ == '__main__':
    play_round_robin(int(sys.argv[1]))