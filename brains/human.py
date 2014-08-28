import random
from components.cards import Card, Color
from components.fight import fight_result


def human_brain_fn(player, game, spied_card):
    if spied_card:
        print 'Opponent is going to play {}'.format(spied_card.name)
    return _input_card(player.color, player.hand)


def _input_card(color, valid_cards):
    ''' Prompts CLI user to enter a card, with retries on validation failure.
    '''

    try:
        _print_hand(valid_cards)
        card_number = raw_input('{} card #: '.format(color.name.title()))
    except NameError:
        print 'Just a number please'
        return _input_card(color, valid_cards)

    try:
        card = Card.get_from_int(int(card_number))
    except (NameError, StopIteration, ValueError):
        print card_number, 'is not a card number. Try again.'
        return _input_card(color, valid_cards)
    else:
        if card in valid_cards:
            print _random_witty_remark(card)
            return card
        else:
            print 'Nice try! You already played your', card.value
            return _input_card(color, valid_cards)


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


CARD_ABBREVIATIONS = ['Mus', 'Pes', 'Spy', 'Asn', 'Amb', 'Wiz', 'Gen', 'Pri']


def _print_hand(cards):
    try:
        numeric_cards = sorted(card.value for card in cards)
        print ' '.join(' {} '.format(card) for card in numeric_cards)
        print ' '.join(CARD_ABBREVIATIONS[card] for card in numeric_cards)
    except IndexError:
        pass


def input_fight():
    '''
    A simple manual-input one-on-one card fight for testing purposes
    '''
    red_card = _input_card(Color.red, Color)
    blue_card = _input_card(Color.blue, Color)

    print 'Result:', fight_result(red_card, blue_card, None, None)

