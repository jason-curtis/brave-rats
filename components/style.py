CLI_COLORS={
    'red': u'\x1b[31m',
    'blue': u'\033[94m',
    'end': u'\033[0m'
    }


def redify(str_):
    return _colorize(str_, 'red')


def blueify(str_):
    return _colorize(str_, 'blue')


def color_pad(str_):
    '''Used to pad a string the same way that a red or blueified string is padded,
    so that it looks the same length'''
    return _colorize(str_, 'end')


def _colorize(str_, color_name):
    '''
    :param str_: String to be colorized
    :param color_name: a color from CLI_COLORS
    :return: str_, wrapped with appropriate flags so that when printed it will be colorized
    '''
    return u'{}{}{}'.format(CLI_COLORS[color_name], str_, CLI_COLORS['end'])
