import unittest

from src.Board import Board
from src.Colour import Colour
from agents.Group17.haswin import has_winning_chain


# NOTE: LLM generated tests not checked by human


class TestWin(unittest.TestCase):
    def setUp(self):
        self.board = Board(11)

    def test_11x11_with_virtual_connection_and_winning_chain(self):
        board_str = (
        """R 0 0 0 0 0 0 0 R R R
            0 R 0 0 0 0 0 0 0 0 0
            0 0 R 0 0 0 0 0 0 0 0
            R 0 R 0 0 0 0 0 0 0 0
            R 0 0 B R 0 0 0 0 0 0
            R 0 0 0 B R 0 0 0 0 0
            R 0 0 0 0 B R 0 0 0 0
            R 0 0 0 0 0 0 R 0 0 0
            R 0 0 0 0 0 0 0 0 0 0
            R 0 0 0 0 0 R 0 0 0 0
            R 0 0 0 0 0 R R 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        # Assert that the board size is 11x11
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertTrue(x)
        self.assertEqual(board.size, 11)
        print(x)
        # Call the has_winning_chain function and verify the RED player has a winning chain
        #self.assertTrue(has_winning_chain(board, Colour.RED))

        # Assert that the BLUE player does not have a winning chain
        #self.assertFalse(has_winning_chain(board, Colour.BLUE))

    def test_empty(self):
        board_str = (
        """0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0
   0 0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0 0
     0 0 0 0 0 0 0 0 0 0 0
      0 0 0 0 0 0 0 0 0 0 0
       0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0
          0 0 0 0 0 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertFalse(x)

    def test_wiggle(self):
        board_str = (
        """0 0 0 0 0 0 0 0 0 R 0
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 R 0 0
        0 0 0 0 0 0 R 0 0 0 0
        0 0 0 0 R 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        R 0 0 0 0 0 0 0 0 0 0
        0 R 0 0 0 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        0 0 0 R 0 0 0 0 0 0 0
        0 0 0 0 R 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertTrue(x)

    def test_wiggle_blocked(self):
        board_str = (
        """0 0 0 0 0 0 0 0 0 R 0
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 R 0 0
        0 0 0 0 0 0 R 0 0 0 0
        0 0 0 0 R 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        R 0 0 0 0 0 0 0 0 0 0
        0 R 0 0 0 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        0 0 0 R R 0 0 0 0 0 0
        0 0 B B B 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertFalse(x)

    def test_top_virtual(self):
        board_str = (
        """0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 R R R R R 0
        0 0 0 0 0 0 0 0 R 0 0
        0 0 0 0 0 0 R 0 0 0 0
        0 0 0 0 R 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        R 0 0 0 0 0 0 0 0 0 0
        0 R 0 0 0 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        0 0 0 R R 0 0 0 0 0 0
        0 0 B B B 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertTrue(x)

    def test_bottom_virtual(self):
        board_str = (
        """0 0 0 0 0 0 R 0 0 0 0
        0 0 0 0 0 R R R R R 0
        0 0 0 0 0 0 0 0 R 0 0
        0 0 0 0 0 0 R 0 0 0 0
        0 0 0 0 R 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        R 0 0 0 0 0 0 0 0 0 0
        0 R 0 0 0 0 0 0 0 0 0
        0 0 R 0 0 0 0 0 0 0 0
        0 0 0 R R R R R R 0 0
        0 0 B B B 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertTrue(x)

    def test_blue_virtual(self):
        board_str = (
        """ B B B 0 0 0 R 0 0 0 0
            0 0 0 B B B B B B B B
            0 0 0 0 0 0 0 0 R 0 0
            0 0 0 0 0 0 R 0 0 0 0
            0 0 0 0 R 0 0 0 0 0 0
            0 0 R 0 0 0 0 0 0 0 0
            R 0 0 0 0 0 0 0 0 0 0
            0 R 0 0 0 0 0 0 0 0 0
            0 0 R 0 0 0 0 0 0 0 0
            0 0 0 R R R R R R 0 0
            0 0 B B B 0 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        print(x)
        self.assertTrue(x)

    def test_blue_right_finish(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 0 B 0 0 0 0 0
            0 0 0 0 0 B B 0 0 0 0
            0 0 0 0 0 B B 0 0 B 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 B B B B B B 0
            0 0 0 B R 0 0 0 0 0 0
            B B B 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertTrue(x)

    def test_blue_left_finish(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 0 B 0 0 0 0 0
            0 0 0 0 0 B B 0 0 0 0
            0 0 0 0 0 B B 0 0 B 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 B B B B B B B
            0 0 0 B R 0 0 0 0 0 0
            0 B B 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertTrue(x)

    def test_red_full(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 R B 0 0 0 0 0
            0 0 0 0 R B B 0 0 0 0
            0 0 0 0 R B B 0 0 B 0
            0 0 0 0 R 0 0 0 0 0 0
            0 0 0 0 R B B B B B B
            0 0 0 B R 0 0 0 0 0 0
            0 B B 0 R 0 0 0 0 0 0
            0 0 0 0 R 0 0 0 0 0 0
            0 0 0 0 R 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.RED)
        self.assertTrue(x)

    def test_blue_full(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 R B 0 0 0 0 0
            0 0 0 0 R B B 0 0 0 0
            0 0 0 0 R B B 0 0 B 0
            0 0 0 0 R 0 0 0 0 0 0
            B B B B B B B B B B B
            0 0 0 B R 0 0 0 0 0 0
            0 B B 0 R 0 0 0 0 0 0
            0 0 0 0 R 0 0 0 0 0 0
            0 0 0 0 R 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertTrue(x)

    def test_blue_no_winning_chain(self):
        board_str = (
            """ R R R R R R R R R R R
                  R R R R R B R R R B R
                    R R R R B R R B B R R
                      B B B R R B B B B R B
                        0 B 0 B B B B B B B 0
                          0 0 0 0 B 0 B B B B 0
                            0 0 R B 0 0 0 0 0 0 0
                              0 0 B 0 0 0 0 0 0 0 0
                                0 0 0 B 0 0 0 0 0 0 0
                                  0 0 0 0 0 0 0 0 0 0 0
                                    B 0 0 B 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertFalse(x)

    def test_blue_no_winning_chain2(self):
        board_str = (
            """ R R R R R R R R R R R
                  R R R R R B R R R B R
                    R R R R B R 0 B B 0 0
                      B B B 0 0 0 B 0 B 0 B
                        0 B 0 0 B B 0 B 0 B 0
                          0 0 0 0 B 0 0 B B B 0
                0 0 R B 0 0 0 0 0 0 0
                0 0 B 0 0 0 0 0 0 0 0
                0 0 0 B 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0
                B 0 0 B 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertFalse(x)

    def test_blue_no_winning_chain3(self):
        board_str = (
            """R R R R R R R R R R R
 R R R R R R R B B B R
  R R R B R R R R R B R
   R R B 0 0 R B 0 0 0 0
    B 0 0 B B B 0 0 B 0 0
     0 0 0 B 0 0 B B 0 0 B
      0 0 B 0 B 0 0 B 0 0 0
       0 0 0 0 B B B B B 0 0
        0 0 0 0 0 0 0 0 0 B 0
         0 B 0 0 0 0 0 0 0 0 B
          0 B 0 B 0 0 0 B 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        x = has_winning_chain(tiles, Colour.BLUE)
        self.assertFalse(x)



if __name__ == "__main__":
    unittest.main()
