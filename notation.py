import os
from player_colors import Colors


class GoNotation:
    def create_new_notation(self, name, board_size, board_komi):
        self.path = os.path.join('parties', f'{name}.GoNotation')
        self.file = open(self.path, 'w', encoding='ascii')
        self.file.write(f'{board_size}_{board_komi}\n')

    def record_move(self, x, y, color):
        self.file.write(f'{color.name[0]}[{x},{y}]_')

    def open_existing(self, path):
        with open(path, 'r', encoding='ascii') as file:
            self.size, self.komi = file.readline()[:-1].split('_')
            self.size = int(self.size)
            self.komi = float(self.komi)
            moves = []
            for move in file.readline().split('_')[:-1]:
                if move[0] == 'b':
                    color = Colors.black
                else:
                    color = Colors.white
                x, y = move[2:-1].split(',')
                moves.append((x, y, color))
            self.main_branch = Branch(moves)
            branches = [self.main_branch]
            for party in file.readlines():
                start, moves = party.split(':')
                while start[0] == 'u':
                    start = start[1:]
                    branches.pop()
                branches.append(branches[-1].added_branch(start, moves))
        return self.main_branch


class Branch:
    def __init__(self, moves):
        self.moves = moves
        self.branches = {}

    def added_branch(self, start, moves):
        if start in self.branches:
            self.branches[start].append(Branch(moves))
        else:
            self.branches[start] = [Branch(moves)]
        return self.branches[start]
