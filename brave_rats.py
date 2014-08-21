from brains.example_ai import random_ai_brain_fn
from brains.human import human_brain_fn
from components.cards import Color
from components.fight import resolve_fight, successful_spy_color
from components.game_status import GameStatus
from components.player import Player


def _get_played_cards(red_player, blue_player, game):
    spy_color = successful_spy_color(game.most_recent_fight)
    if spy_color == Color.red:
        # Red gets to peek at Blue's card
        blue_card = blue_player.choose_and_play_card(game)
        red_card = red_player.choose_and_play_card(game, blue_card)
    elif spy_color == Color.blue:
        # Blue gets to peek at Red's card
        red_card = red_player.choose_and_play_card(game)
        blue_card = blue_player.choose_and_play_card(game, red_card)
    else:
        red_card, blue_card = red_player.choose_and_play_card(game), blue_player.choose_and_play_card(game)
    return red_card, blue_card


def play_game(red_brain_fn=random_ai_brain_fn, blue_brain_fn=human_brain_fn):
    game = GameStatus()
    red_player = Player(Color.red, brain_fn=red_brain_fn)
    blue_player = Player(Color.blue, brain_fn=blue_brain_fn)

    while not game.is_over:
        red_card, blue_card = _get_played_cards(red_player, blue_player, game)
        resolve_fight(red_card, blue_card, game)
        print game.score_summary

    # Game's over when while loop exits
    if game.winner:
        print game.winner.name.title(), 'wins!'
    else:
        print 'tie!'

    return game


if __name__ == '__main__':
    while True:
        play_game()
