import argparse
from engine import GoEngine
from player_colors import Colors


def path(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print('Invalid file path')
        raise ValueError(path)
    except FileExistsError:
        print('FileExistsError')
        raise ValueError(path)


def size(size):
    size = int(size)
    if 0 < size < 100:
        return size
    else:
        raise ValueError(size)


def komi(value):
    value = float(value)
    if value >= 0:
        return value
    else:
        raise ValueError(value)


def color(value):
    if value == 'w' or value == 'white':
        return Colors.white
    elif value == 'b' or value == 'black':
        return Colors.black
    else:
        raise ValueError(value)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='application functionality')

game_parser = subparsers.add_parser('play', help='to start playing')
game_parser.add_argument('-o', '--opponent', type=color, default=None,
                         help='color of your stones in a game with a '
                              'computer opponent (if you want to play with a '
                              'computer opponent)')
game_parser.add_argument('-s', '--size', type=size, default=19,
                         help='the board size for the game (default 19)')
game_parser.add_argument('-k', '--komi', type=komi, default=6.5,
                         help='handicap for white (default 6.5)')

analysis_parser = subparsers.add_parser('analysis',
                                        help='analysis of games played')
analysis_parser.add_argument('path', type=path, help='path to game notation')

args = parser.parse_args()

try:
    x = GoEngine(args.size, args.komi)
    x.start(not bool(args.opponent), args.opponent)
except AttributeError:
    print(args.path)
