import unittest

from src.Board import Board
from src.Colour import Colour

# NOTE: LLM generated tests not checked by human


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(11)

    def test_board_initialization(self):
        self.assertEqual(self.board.size, 11)
        self.assertIsNone(self.board.get_winner())

    def test_set_tile_colour(self):
        self.board.set_tile_colour(0, 0, Colour.RED)
        self.assertEqual(self.board.tiles[0][0].colour, Colour.RED)

    def test_from_string(self):
        board_str = "R B 0\nB R 0\n0 0 0"
        board = Board.from_string(board_str, board_size=3)
        self.assertEqual(board.size, 3)
        self.assertEqual(board.tiles[0][0].colour, Colour.RED)
        self.assertEqual(board.tiles[0][1].colour, Colour.BLUE)

    def test_has_ended_red_win(self):
        for i in range(11):
            self.board.set_tile_colour(i, 0, Colour.RED)
        self.assertTrue(self.board.has_ended(Colour.RED))
        self.assertEqual(self.board.get_winner(), Colour.RED)

    def test_has_ended_blue_win(self):
        for i in range(11):
            self.board.set_tile_colour(0, i, Colour.BLUE)
        self.assertTrue(self.board.has_ended(Colour.BLUE))
        self.assertEqual(self.board.get_winner(), Colour.BLUE)

    def test_board_equality(self):
        board1 = Board(5)
        board2 = Board(5)
        self.assertEqual(board1, board2)
        board1.set_tile_colour(0, 0, Colour.RED)
        self.assertNotEqual(board1, board2)


if __name__ == "__main__":
    unittest.main()
