import random


def random_ai_brain_fn(player, game, spied_card):
    '''The most sophisticated Brave Rats AI ever written

    :param player: a Player instance
    :param game: a Game instance, used to look up info about played cards, score, etc.
    :param spied_card: If I successfully played a spy last turn, this is the card that the opponent has revealed and
        will play. Otherwise, None
    :return: a card from my player's hand with which to vanquish my opponent.
    '''
    if spied_card:
        print 'Hah! You think you can beat me with that {}? Prepare to be CRUSHED!'.format(spied_card.name)
    return random.choice(player.hand)
