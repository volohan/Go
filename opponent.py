import copy
from player_colors import Colors


class GoOpponentAI:
    def __init__(self, board, color):
        self.color = color
        self.board = board
        self.depth = 3

    def add_breath(self, x, y, moves, board):
        for i, j in board.shifts_to_neighbors:
            field = board.get_field(x + i, y + j)
            if field:
                if field not in self.visited:
                    self.visited.add(field)
                    self.add_breath(x + i, y + j, moves, board)
            elif field is not None:
                moves.add((x + i, y + j))

    def find_moves(self, board):
        moves = set()
        self.visited = set()
        for y in range(1, board.size + 1):
            for x in range(1, board.size + 1):
                field = board.get_field(x, y)
                if field and field not in self.visited:
                    self.visited.add(field)
                    self.add_breath(x, y, moves, board)
        return moves

    def get_move(self):
        moves = self.find_moves(self.board)
        try:
            self.depth = 20 / len(moves)
        except ZeroDivisionError:
            pass
        if self.depth < 3:
            self.depth = 3

        new_move = (0, None)
        if len(moves) != 0:
            for x, y in moves:
                fake_board = copy.deepcopy(self.board)
                if fake_board.make_move(x, y, self.color):
                    next_moves = copy.deepcopy(moves)
                    next_moves.discard((x, y))
                    rank = self.try_move(1, fake_board, Colors(-self.color))
                    print(f'*', end='')
                    if not new_move[1]:
                        new_move = (rank, (x, y))
                    elif rank >= new_move[0]:
                        new_move = (rank, (x, y))

        else:
            fake_board = copy.deepcopy(self.board)
            if fake_board.make_move(self.board.size // 2,
                                    self.board.size // 2, self.color):
                new_move = (0, (self.board.size // 2, self.board.size // 2))

        print()
        return new_move[1]

    def try_move(self, depth, board, color):
        if depth < self.depth:
            res = 0
            bad_moves = 0
            moves = self.find_moves(board)
            for x, y in moves:

                new_board = copy.deepcopy(board)

                if new_board.make_move(x, y, color):
                    res += self.try_move(depth + 1, new_board,
                                         Colors(-color))
                else:
                    bad_moves += 1

            if bad_moves == len(moves) and bad_moves != 0:
                if color == self.color:
                    res = board.scores[self.color] \
                          - board.scores[Colors(-self.color)]
                else:
                    res = board.scores[self.color] \
                          - board.scores[Colors(-self.color)]
            else:
                return res
        else:
            res = board.scores[self.color] - board.scores[Colors(-self.color)]

        return res * (self.depth + 1 - depth)
