import unittest
from board import Goban
from player_colors import Colors


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Goban(9, 0)

    def test_simple_1(self):
        self.board.make_move(1, 3, Colors.black)

        self.board.make_move(2, 2, Colors.black)
        self.board.make_move(2, 4, Colors.black)
        self.board.make_move(2, 5, Colors.black)
        self.board.make_move(2, 6, Colors.black)
        self.board.make_move(2, 7, Colors.black)
        self.board.make_move(2, 8, Colors.black)
        self.board.make_move(2, 9, Colors.black)

        self.board.make_move(3, 1, Colors.black)
        self.board.make_move(3, 2, Colors.black)
        self.board.make_move(3, 3, Colors.black)
        self.board.make_move(3, 4, Colors.white)
        self.board.make_move(3, 5, Colors.white)
        self.board.make_move(3, 6, Colors.white)
        self.board.make_move(3, 7, Colors.white)
        self.board.make_move(3, 8, Colors.white)
        self.board.make_move(3, 9, Colors.white)

        self.board.make_move(4, 1, Colors.white)
        self.board.make_move(4, 2, Colors.white)
        self.board.make_move(4, 3, Colors.white)
        self.board.make_move(4, 4, Colors.white)
        self.board.make_move(4, 7, Colors.white)

        self.board.make_move(5, 5, Colors.white)
        self.board.make_move(5, 6, Colors.white)
        self.board.make_move(5, 7, Colors.black)
        self.board.make_move(5, 8, Colors.white)
        self.board.make_move(5, 9, Colors.white)

        self.board.make_move(6, 1, Colors.white)
        self.board.make_move(6, 3, Colors.white)
        self.board.make_move(6, 4, Colors.white)
        self.board.make_move(6, 5, Colors.white)
        self.board.make_move(6, 6, Colors.black)
        self.board.make_move(6, 7, Colors.black)
        self.board.make_move(6, 8, Colors.black)
        self.board.make_move(6, 9, Colors.black)

        self.board.make_move(7, 2, Colors.white)
        self.board.make_move(7, 3, Colors.white)
        self.board.make_move(7, 4, Colors.black)
        self.board.make_move(7, 5, Colors.black)
        self.board.make_move(7, 7, Colors.black)

        self.board.make_move(8, 3, Colors.white)
        self.board.make_move(8, 4, Colors.black)
        self.board.make_move(8, 6, Colors.black)

        self.board.make_move(9, 3, Colors.white)
        self.board.make_move(9, 4, Colors.black)
        self.assertEqual(self.board.score(True),
                         {Colors.white: 14, Colors.black: 22})

    def test_simple_2(self):
        self.board.make_move(1, 5, Colors.black)
        self.board.make_move(1, 6, Colors.black)
        self.board.make_move(1, 7, Colors.black)
        self.board.make_move(1, 8, Colors.black)

        self.board.make_move(2, 4, Colors.black)
        self.board.make_move(2, 6, Colors.black)
        self.board.make_move(2, 7, Colors.white)
        self.board.make_move(2, 8, Colors.black)
        self.board.make_move(2, 9, Colors.black)

        self.board.make_move(3, 6, Colors.black)
        self.board.make_move(3, 7, Colors.white)
        self.board.make_move(3, 8, Colors.black)

        self.board.make_move(3, 1, Colors.black)
        self.board.make_move(3, 2, Colors.black)
        self.board.make_move(3, 3, Colors.black)
        self.board.make_move(3, 6, Colors.black)
        self.board.make_move(3, 7, Colors.white)
        self.board.make_move(3, 8, Colors.black)

        self.board.make_move(4, 1, Colors.white)
        self.board.make_move(4, 2, Colors.white)
        self.board.make_move(4, 3, Colors.black)
        self.board.make_move(4, 6, Colors.black)
        self.board.make_move(4, 7, Colors.white)
        self.board.make_move(4, 8, Colors.black)
        self.board.make_move(4, 9, Colors.black)

        self.board.make_move(5, 2, Colors.white)
        self.board.make_move(5, 3, Colors.black)
        self.board.make_move(5, 4, Colors.black)
        self.board.make_move(5, 5, Colors.black)
        self.board.make_move(5, 6, Colors.black)
        self.board.make_move(5, 7, Colors.white)
        self.board.make_move(5, 8, Colors.white)
        self.board.make_move(5, 9, Colors.white)

        self.board.make_move(6, 2, Colors.white)
        self.board.make_move(6, 3, Colors.black)
        self.board.make_move(6, 4, Colors.white)
        self.board.make_move(6, 5, Colors.white)
        self.board.make_move(6, 6, Colors.white)

        self.board.make_move(7, 2, Colors.white)
        self.board.make_move(7, 3, Colors.white)
        self.board.make_move(7, 7, Colors.white)
        self.board.make_move(7, 8, Colors.white)
        self.board.make_move(7, 9, Colors.white)

        self.board.make_move(8, 4, Colors.white)

        self.assertEqual(self.board.score(True),
                         {Colors.white: 26, Colors.black: 14})

    def test_dead_stone(self):
        self.board.make_move(1, 2, Colors.black)
        self.board.make_move(1, 4, Colors.black)
        self.board.make_move(1, 5, Colors.white)
        self.board.make_move(1, 6, Colors.black)

        self.board.make_move(2, 1, Colors.white)
        self.board.make_move(2, 2, Colors.black)
        self.board.make_move(2, 3, Colors.black)
        self.board.make_move(2, 4, Colors.black)
        self.board.make_move(2, 5, Colors.white)
        self.board.make_move(2, 6, Colors.white)
        self.board.make_move(2, 7, Colors.white)
        self.board.make_move(2, 8, Colors.white)
        self.board.make_move(2, 9, Colors.white)

        self.board.make_move(3, 1, Colors.black)
        self.board.make_move(3, 2, Colors.black)
        self.board.make_move(3, 3, Colors.white)
        self.board.make_move(3, 4, Colors.black)
        self.board.make_move(3, 5, Colors.white)
        self.board.make_move(3, 6, Colors.black)
        self.board.make_move(3, 7, Colors.black)
        self.board.make_move(3, 8, Colors.black)
        self.board.make_move(3, 9, Colors.black)

        self.board.make_move(4, 3, Colors.white)
        self.board.make_move(4, 4, Colors.black)
        self.board.make_move(4, 5, Colors.white)
        self.board.make_move(4, 6, Colors.black)
        self.board.make_move(4, 8, Colors.black)

        self.board.make_move(5, 1, Colors.black)
        self.board.make_move(5, 2, Colors.black)
        self.board.make_move(5, 3, Colors.black)
        self.board.make_move(5, 4, Colors.black)
        self.board.make_move(5, 5, Colors.white)
        self.board.make_move(5, 6, Colors.black)
        self.board.make_move(5, 7, Colors.black)
        self.board.make_move(5, 8, Colors.black)
        self.board.make_move(5, 9, Colors.white)

        self.board.make_move(6, 1, Colors.white)
        self.board.make_move(6, 2, Colors.white)
        self.board.make_move(6, 3, Colors.white)
        self.board.make_move(6, 4, Colors.white)
        self.board.make_move(6, 5, Colors.white)
        self.board.make_move(6, 7, Colors.white)
        self.board.make_move(6, 8, Colors.white)
        self.board.make_move(6, 9, Colors.white)

        self.board.make_move(7, 3, Colors.white)
        self.board.make_move(7, 4, Colors.black)
        self.board.make_move(7, 5, Colors.white)
        self.board.make_move(7, 6, Colors.white)
        self.board.make_move(7, 7, Colors.white)
        self.board.make_move(7, 8, Colors.black)
        self.board.make_move(7, 9, Colors.black)

        self.board.make_move(8, 2, Colors.white)
        self.board.make_move(8, 3, Colors.white)
        self.board.make_move(8, 4, Colors.black)
        self.board.make_move(8, 5, Colors.black)
        self.board.make_move(8, 6, Colors.black)
        self.board.make_move(8, 7, Colors.black)
        self.board.make_move(8, 8, Colors.black)

        self.board.make_move(9, 3, Colors.white)
        self.board.make_move(9, 4, Colors.black)
        self.board.make_move(9, 5, Colors.white)
        self.board.make_move(9, 6, Colors.white)
        self.board.make_move(9, 8, Colors.black)

        print(self.board.get_map())
        self.assertEqual(self.board.score(True),
                         {Colors.white: 31, Colors.black: 17})


if __name__ == '__main__':
    unittest.main()
