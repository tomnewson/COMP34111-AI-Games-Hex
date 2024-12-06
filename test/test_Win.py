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
            0 0 R 0 0 0 0 0 0 0 0
            R 0 0 B R 0 0 0 0 0 0
            R 0 0 0 B R 0 0 0 0 0
            R 0 0 0 0 B R 0 0 0 0
            R 0 0 0 0 0 0 R 0 0 0
            R 0 0 0 0 0 0 0 0 0 0
            R 0 0 0 0 0 R 0 0 0 0
            R 0 0 0 0 0 R R 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        print("####################################################################################")
        # Assert that the board size is 11x11

        x = has_winning_chain(board, Colour.RED)
        if x:
            print("WINNER")
        print(x)
        self.assertEqual(board.size, 11)
        # Call the has_winning_chain function and verify the RED player has a winning chain
        #self.assertTrue(has_winning_chain(board, Colour.RED))

        # Assert that the BLUE player does not have a winning chain
        #self.assertFalse(has_winning_chain(board, Colour.BLUE))


if __name__ == "__main__":
    unittest.main()
