import copy

from player_colors import Colors
from stones import Goishi


class Goban:
    def __init__(self, size, komi):
        self.size = size
        self.map = []
        for i in range(size):
            self.map.append([])
            for j in range(size):
                self.map[i].append(0)
        self.komi = komi
        self.checks = set()
        self.shifts_to_neighbors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.ko_rule = None

    def get_field(self, first, second):
        try:
            return self.map[self.size - second][first - 1]
        except IndexError:
            return None

    def set_field(self, first, second, stone):
        if stone:
            self.map[self.size - second][first - 1] = stone
        else:
            self.map[self.size - second][first - 1] = 0

    def make_move(self, x, y, color):
        if not self.get_field(x, y):

            res = True
            self.set_field(x, y, Goishi(x, y, color))
            for i, j in self.shifts_to_neighbors:
                if self.get_field(x + i, y + j) \
                        and self.get_field(x + i, y + j).color != color:
                    self.try_take(x + i, y + j, Colors(-color))
            if self.check_for_take(x, y, color):
                res = False
                self.set_field(x, y, None)
            self.leave()

            return res
        else:
            return False

    def try_take(self, x, y, color):
        if self.check_for_take(x, y, color):
            self.take()
            return True
        else:
            self.leave()
            return False

    def check_for_take(self, x, y, color):
        if 0 < x <= self.size and 0 < y <= self.size:
            field = self.get_field(x, y)
            if field:
                if field.color == color:
                    self.checks.add(field)
                    field.is_surrounded = True
                    for i, j in self.shifts_to_neighbors:
                        if self.get_field(x + i, y + j) not in self.checks:
                            field.is_surrounded &= \
                                self.check_for_take(x + i, y + j, color)
                    return field.is_surrounded
                else:
                    return True
            else:
                return False
        else:
            return True

    def take(self):
        for row in self.map:
            for field in row:
                if field and field.is_surrounded:
                    self.set_field(field.x, field.y, None)
        self.checks = set()

    def leave(self):
        for row in self.map:
            for field in row:
                if field:
                    field.is_surrounded = False
        self.checks = set()

    def score(self):
        self.continuation_of_game = copy.deepcopy(self.map)
        empty = set([(x, y) for y in range(1, self.size + 1)
                     for x in range(1, self.size + 1) if self.get_field(x, y)])
        for x, y in empty:
            pass

    def finish_move(self):
        pass

    def get_map(self):
        res = ''
        for y in range(self.size):
            res += str(self.size - y) + ' '
            for x in range(self.size):
                field = self.map[y][x]
                if field:
                    res += field.image
                else:
                    res += '+'
                    #res += '✛'
            res += '\n'
        res += '  '
        for i in range(self.size):
            res += str(i + 1)
        res += '\n'
        return res
