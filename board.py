import numpy
from player_colors import Colors
from stones import Goishi


class Goban:
    def __init__(self, size, komi):
        self.map = numpy.zeros((size, size))
        self.komi = komi
        self.shifts_to_neighbors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.ko_rule = set()

    def get_field(self, first, second):
        return self.map[19 - second, first]

    def set_field(self, first, second, stone):
        if stone:
            self.map[19 - second, first] = stone
        else:
            self.map[19 - second, first] = 0

    def make_move(self, x, y, color):
        if not self.get_field(x, y):
            self.set_field(x, y, Goishi(color))

            self.is_enemy_eye = True
            self.checks = set()
            for i, j in self.shifts_to_neighbors:
                if self.get_field(x + i, y + j).color != color:
                    self.is_enemy_eye &= \
                        not self.check_for_take(x + i, y + j, Colors(-color))
                else:
                    self.is_enemy_eye = False

            if self.is_enemy_eye:
                self.set_field(x, y, None)
                return False

            return True
        else:
            return False

    def check_for_take(self, x, y, color):
        if 0 < x < self.map.size + 1 and 0 < y < self.map.size + 1:
            field = self.get_field(x, y)
            if field:
                if field.color == color:
                    self.checks.add(field)
                    is_surrounded = True
                    for i, j in self.shifts_to_neighbors:
                        if self.get_field(x + i, y + j) not in self.checks:
                            is_surrounded &= \
                                self.check_for_take(x + i, y + j, color)
                    return is_surrounded
                else:
                    return True
            else:
                return False

    def is_there_move(self):
        pass

    def score(self):
        pass

    def get_map(self):
        pass
