def print_colored(text, color):
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
    }
    if color not in colors:
        raise ValueError(f'Invalid color: {color}')
    print(f'\033[{colors[color]}m{text}\033[0m')
