CLI_COLORS={
    'red': '\x1b[31m',
    'blue': '\033[94m',
    'end': '\033[0m'
    }


def redify(str_):
    return _colorize(str_, 'red')


def blueify(str_):
    return _colorize(str_, 'blue')


def _colorize(str_, color_name):
    '''
    :param str_: String to be colorized
    :param color_name: a color from CLI_COLORS
    :return: str_, wrapped with appropriate flags so that when printed it will be colorized
    '''
    return '{}{}{}'.format(CLI_COLORS[color_name], str_, CLI_COLORS['end'])
