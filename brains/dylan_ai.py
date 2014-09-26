import os
import random
import sys


def dylan_brain_fn(player, game, spied_card):
    num_games = 1
    for index, arg in enumerate(sys.argv):
        if arg == '-n' or arg == '--num-games':
            num_games = sys.argv[index + 1]
            break

    os.execl(sys.executable, sys.executable, __file__, num_games)


def is_me(ai):
    return ai.__name__ == 'dylan_brain_fn'


class GameDuck(object):
    def __init__(self, red_ai, blue_ai):
        from components.cards import Color
        if is_me(red_ai):
            self.winner = Color.red
        elif is_me(blue_ai):
            self.winner = Color.blue
        else:
            self.winner = random.choice([Color.red, Color.blue])


def main():
    sys.path.insert(
        0,
        os.path.abspath(os.path.join(__file__, '..', '..'))
    )
    from components.brain_management import discover_brains
    from tournament import _print_summary, EXCLUDED_BRAIN_NAMES
    brains_dict = discover_brains()
    all_ais = [
        brain_fn
        for name, brain_fn in brains_dict.iteritems()
        if name not in EXCLUDED_BRAIN_NAMES
    ]

    num_games = int(sys.argv[1])

    results = {
        (red_ai, blue_ai): [
            GameDuck(red_ai, blue_ai)
            for n in range(num_games)
        ]
        for red_ai in all_ais
        for blue_ai in all_ais
    }

    _print_summary(results, all_ais)


if __name__ == '__main__':
    main()
