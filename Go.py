import argparse

from engine import GoEngine


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
    if size % 2 != 0 and 0 < size < 100:
        return size
    else:
        raise ValueError(size)


def komi(value):
    value = float(value)
    if value >= 0:
        return value
    else:
        raise ValueError(value)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='application functionality')

game_parser = subparsers.add_parser('play', help='to start playing')
game_parser.add_argument('opponent', type=bool,
                         help='against the computer? [True/False]')
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
    x.start(args.opponent)
except AttributeError:
    print(args.path)
