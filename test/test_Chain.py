import unittest

from src.Board import Board
from src.Colour import Colour
from agents.Group17.chain import ChainFinder

class TestChain(unittest.TestCase):
    def test_red_side_wiggle(self):
        board_str = (
        """ R 0 0 0 0 0 0 0 R R R
             0 R 0 0 0 0 0 0 0 0 0
              0 0 R 0 0 0 0 0 0 0 0
               R 0 0 0 0 0 0 0 0 0 0
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
        self.assertCountEqual(virtuals, [((0,1), (0,2)),((2,1), (2,0))])

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
        self.assertCountEqual(virtuals, [((2,5), (3,4))])

    def test_direct_chain_ignores_edge(self):
        board_str = (
        """ 0 R 0 0 0 0 0 0 0 0 0 
            0 0 0 0 0 0 0 0 R 0 R 
            0 0 0 0 0 0 0 B R B 0 
            0 0 0 0 0 B 0 R B 0 0 
            0 0 R 0 0 B R B 0 0 0 
            0 0 0 R 0 0 B 0 0 0 0 
            0 0 0 R B B R 0 R R 0 
            0 0 R 0 R B 0 R 0 0 0 
            0 0 R R B R B R B 0 B 
            0 B B B B R B R R 0 R 
            B R 0 0 B B 0 0 0 B 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search(False)
        self.assertFalse(found)

        tiles[2][10] = Colour.BLUE
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search(False)
        self.assertTrue(found)


    def test_blue_right_drop_wiggle(self):
        board_str = (
        """ R R R R R R R R R R R
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
        self.assertCountEqual(virtuals, [((9,1), (9,2)), ((5,8), (6,7)), ((5,10), (6,10))])

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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertFalse(found)

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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertFalse(found)

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
        0 0 0 R R R 0 0 0 0 0
        0 0 B B B R 0 0 0 0 0 """
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

    def test_blue_right_finish(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 0 B 0 0 0 0 0
            0 0 0 0 0 B B 0 0 0 0
            0 0 0 0 0 B B 0 0 B 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 B B B B B B 0
            0 0 0 B 0 0 0 0 0 0 0
            B B B 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

    def test_blue_left_finish(self):
        board_str = (
        """ R R R R R R R R R R R
            R R R R R B R B R R 0
            B 0 0 0 0 B 0 0 0 0 0
            0 0 0 0 0 B B 0 0 0 0
            0 0 0 0 0 B B 0 0 B 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 B B B B B B B
            0 0 0 B 0 0 0 0 0 0 0
            0 B B 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0
            0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

    def test_red_full_virtuals_disabled(self):
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
        chain_finder = ChainFinder(tiles, Colour.RED)
        found, virtuals = chain_finder.search(False)
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

    def test_blue_full_wiggle(self):
        board_str = (
        """R R R R R R B R B R R
            R R R R R R R R R R R
             B R B R R B R R B B B
              R R B B 0 0 0 B B 0 B
               B 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0
                 0 R 0 0 B 0 0 0 0 B B
                  0 B 0 0 0 0 0 B B 0 0
                   0 0 B B B B B 0 0 0 0
                    B B 0 0 0 0 0 0 0 0 0
                     0 0 0 0 0 0 0 0 0 B 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        tiles = [[tile.colour for tile in row] for row in board.tiles]
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertTrue(found)

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
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertFalse(found)

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
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertFalse(found)

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
        chain_finder = ChainFinder(tiles, Colour.BLUE)
        found, virtuals = chain_finder.search()
        self.assertFalse(found)

if __name__ == "__main__":
    unittest.main()
