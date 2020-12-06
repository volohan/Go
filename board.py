import copy
from player_colors import Colors
from stones import Goishi


class Goban:
    def __init__(self, size, komi):
        self.size = size
        self.map = []
        self.scores = {Colors.white: 0, Colors.black: 0}
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
            self.set_field(x, y, Goishi(x, y, color))
            res = True
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
                    self.scores[field.color] += 1
                    self.set_field(field.x, field.y, None)
        self.checks = set()

    def leave(self):
        for row in self.map:
            for field in row:
                if field:
                    field.is_surrounded = False
        self.checks = set()

    def find_territory(self, x, y, ignore_color):
        if 0 < x <= self.size and 0 < y <= self.size:
            field = self.get_field(x, y)
            if not field or field.color == ignore_color:
                try:
                    color = field.color
                except AttributeError:
                    color = None
                self.checks.add((x, y, color))
                self.visited.add((x, y))
                for i, j in self.shifts_to_neighbors:
                    field = self.get_field(x + i, y + j)
                    try:
                        color = field.color
                    except AttributeError:
                        color = None
                    if (x + i, y + j, color) not in self.checks:
                        self.find_territory(x + i, y + j, ignore_color)

    def try_to_play_to_capture(self, deep, color, moves):
        if deep < 5:
            res = True
            if color != self.attack_color:
                res &= self.try_to_play_to_capture(deep + 1, Colors(-color),
                                                   copy.deepcopy(moves))
            bad_moves = 0
            for x, y in copy.deepcopy(moves).pop():
                map = copy.deepcopy(self.map)
                scores = copy.deepcopy(self.scores)

                if self.make_move(x, y, color):
                    res &= self.try_to_play_to_capture(deep + 1,
                                                       Colors(-color),
                                                       copy.deepcopy(moves))
                else:
                    bad_moves += 1

                self.map = map
                self.scores = scores
            if bad_moves == len(moves):
                return False
            else:
                return res
        else:
            return False

    def find_and_finish_playing_conflict_zones(self, x, y, attack_color):
        self.checks = set()
        self.find_territory(x, y, Colors(-attack_color))
        if len(self.checks) < self.size * self.size / 2:
            original_position = copy.deepcopy(self.checks)
            possibility_moves = set()
            for x, y, color in self.checks:
                if not color:
                    possibility_moves.add((x, y))
            if len(original_position) != len(possibility_moves):
                self.attack_color = attack_color
                self.try_to_play_to_capture(0, attack_color,
                                            possibility_moves)

    def take_dead_stones(self):
        self.visited = set()
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) not in self.visited and not self.get_field(x, y):
                    self.find_and_finish_playing_conflict_zones(x, y,
                                                                Colors.white)
                    self.find_and_finish_playing_conflict_zones(x, y,
                                                                Colors.black)

    def to_tile_neutral_field(self):
        pass

    def add_captured_territory(self):
        pass

    def score(self, game_is_end):
        if game_is_end:
            self.take_dead_stones()
            self.to_tile_neutral_field()
            self.add_captured_territory()
        return self.scores

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
                    # res += '✛'
            res += '\n'
        res += '  '
        for i in range(self.size):
            res += str(i + 1)
        res += '\n'
        return res
