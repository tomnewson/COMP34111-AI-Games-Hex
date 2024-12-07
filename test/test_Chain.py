import unittest

from src.Board import Board
from src.Colour import Colour
from agents.Group17.chain import ChainFinder


# NOTE: LLM generated tests not checked by human


class TestWin(unittest.TestCase):
    def test_11x11_with_virtual_connection_and_winning_chain(self):
        board_str = (
        """ R 0 0 0 0 0 0 0 R R R
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
        self.assertEqual(board.size, 11)
        
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)
        self.assertListEqual(virtuals, [((0,1), (1,0))])

    def test_blue(self):
        board_str = (
        """ R 0 0 0 0 0 0 0 R R R
             0 R 0 0 0 0 0 0 0 0 0
              B B B B B 0 0 0 0 0 0
               R 0 R 0 0 B B B B B B
                R 0 0 0 R 0 0 0 0 0 0
            R 0 0 0 B R 0 0 0 0 0
            R 0 0 0 0 B R 0 0 0 0
            R 0 0 0 0 0 0 R 0 0 0
            R 0 0 0 0 0 0 0 0 0 0
            R 0 0 0 0 0 R 0 0 0 0
            R 0 0 0 0 0 R R 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)
        self.assertListEqual(virtuals, [((2,5), (3,4))])

    def test_x(self):
        board_str = (
        """R R R R R R R R R R R 
        R R B R R R R R B R R 
        R R R R 0 0 0 B 0 0 0 
        0 0 0 0 0 B 0 0 0 B 0 
        0 B 0 B B B B 0 0 0 B 
        0 0 0 0 0 0 B B 0 0 0 
        0 0 0 0 0 B 0 0 B B 0 
        0 0 0 B B R 0 0 0 0 0 
        0 0 B 0 0 B 0 0 0 0 0 
        0 0 0 0 0 0 0 0 0 0 0 
        B B B 0 0 0 0 0 0 B 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)
        self.assertListEqual(virtuals, [((2,5), (3,4))])



if __name__ == "__main__":
    unittest.main()
