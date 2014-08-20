from brains.example_ai import random_ai_brain_fn
from brains.human import human_brain_fn
from components.cards import Color
from components.fight import resolve_fight
from components.game_status import GameStatus
from components.player import Player


def play_game(red_brain_fn=random_ai_brain_fn, blue_brain_fn=human_brain_fn):
    game = GameStatus()
    red_player = Player(Color.red, brain_fn=red_brain_fn)
    blue_player = Player(Color.blue, brain_fn=blue_brain_fn)

    while red_player.has_cards() and not game.winner:
        red_card, blue_card = red_player.choose_and_play_card(game), blue_player.choose_and_play_card(game)
        resolve_fight(red_card, blue_card, game)
        print game.score_summary

    # Game's over when while loop exits
    if game.winner:
        print game.winner.name.title(), 'wins!'
    else:
        print 'tie!'
        return


if __name__ == '__main__':
    while True:
        play_game()
