import copy
from player_colors import Colors
from stones import Goishi


class Goban:
    def __init__(self, size, komi):
        self.size = size
        self.depth_of_analysis = 8
        self.map = []
        self.scores = {Colors.white: 0, Colors.black: 0}
        for i in range(size):
            self.map.append([])
            for j in range(size):
                self.map[i].append(0)
        self.komi = komi
        self.checks = set()
        self.boundary = set()
        self.shifts_to_neighbors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.ko_rule = None

    def get_field(self, x, y):
        first = self.size - y
        second = x - 1
        if 0 <= first < self.size and 0 <= second < self.size:
            return self.map[first][second]
        else:
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
                    self.scores[Colors(-field.color)] += 1
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
                for i, j in self.shifts_to_neighbors:
                    field = self.get_field(x + i, y + j)
                    try:
                        color = field.color
                    except AttributeError:
                        color = None
                    if (x + i, y + j, color) not in self.checks:
                        self.find_territory(x + i, y + j, ignore_color)
            else:
                self.boundary.add(field.color)

    def try_to_play_to_capture(self, depth, color, moves):
        if depth < self.depth_of_analysis:
            res = True
            if color != self.attack_color and len(moves) != 0:
                res &= self.try_to_play_to_capture(depth + 1, Colors(-color),
                                                   copy.deepcopy(moves))
            bad_moves = 0
            for x, y in moves:
                if not res:
                    break

                map = copy.deepcopy(self.map)
                scores = copy.deepcopy(self.scores)

                if self.make_move(x, y, color):
                    next_moves = copy.deepcopy(moves)
                    next_moves.discard((x, y))
                    res &= self.try_to_play_to_capture(depth + 1,
                                                       Colors(-color),
                                                       next_moves)
                else:
                    bad_moves += 1

                self.map = map
                self.scores = scores
            if bad_moves == len(moves) and bad_moves != 0:
                if color == self.attack_color:
                    return False
                else:
                    return True
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
            for x, y, color in original_position:
                if not color:
                    possibility_moves.add((x, y))
            if len(original_position) != len(possibility_moves):
                self.attack_color = attack_color
                if self.try_to_play_to_capture(0, attack_color, possibility_moves):
                    for x, y, _ in [i for i in original_position
                                    if (i[0], i[1]) not in possibility_moves]:
                        self.set_field(x, y, None)
                        self.visited.add((x, y, None))
                        self.scores[attack_color] += 1

    def take_dead_stones(self):
        self.visited = set()
        for y in range(1, self.size + 1):
            for x in range(1, self.size + 1):
                if (x, y, None) not in self.visited and not self.get_field(x, y):
                    self.find_territory(x, y, None)
                    self.visited |= self.checks
                    self.find_and_finish_playing_conflict_zones(x, y,
                                                                Colors.white)
                    self.find_and_finish_playing_conflict_zones(x, y,
                                                                Colors.black)

    def to_tile_neutral_field(self):
        self.visited = set()
        for y in range(1, self.size + 1):
            for x in range(1, self.size + 1):
                if (x, y) not in self.visited and not self.get_field(x, y):
                    self.checks = set()
                    self.boundary = set()
                    self.find_territory(x, y, None)
                    if len(self.boundary) == 2:
                        for field in self.checks:
                            self.set_field(field[0], field[1],
                                           Goishi(field[0], field[1],
                                                  Colors.black))

    def add_captured_territory(self):
        self.visited = set()
        for y in range(1, self.size + 1):
            for x in range(1, self.size + 1):
                if (x, y, None) not in self.visited and not self.get_field(x, y):
                    self.checks = set()
                    self.boundary = set()
                    self.find_territory(x, y, None)
                    self.visited |= self.checks
                    if len(self.checks) < self.size * self.size / 2:
                        self.scores[self.boundary.pop()] += len(self.checks)

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
            res += '\n'
        res += '  '
        for i in range(self.size):
            res += str(i + 1)
        res += '\n'
        return res
