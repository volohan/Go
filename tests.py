import unittest
from board import Goban
from player_colors import Colors


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Goban(9, 0)

    def test_something(self):
        self.board.make_move(1, 2, Colors.black)
        self.board.make_move(2, 1, Colors.black)
        self.board.make_move(2, 3, Colors.black)
        self.board.make_move(3, 2, Colors.black)
        self.board.make_move(2, 2, Colors.white)
        print(self.board.map)


if __name__ == '__main__':
    unittest.main()
