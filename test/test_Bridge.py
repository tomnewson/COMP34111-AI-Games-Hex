import unittest

from src.Board import Board
from src.Colour import Colour
from agents.Group17.bridgeDefender import BridgeDefender

class TestBridge(unittest.TestCase):
    def test1(self):
        board_str = (
            """0 0 0 0 0 0 0 0 0 0 0 
                0 0 0 0 0 0 0 0 0 0 0 
                 0 0 0 0 0 0 0 0 0 0 0 
                  0 0 0 0 0 0 0 0 0 0 0 
                   0 0 0 0 0 0 0 R 0 0 0 
                    0 0 0 0 0 R B 0 0 0 0 
                     0 0 0 0 0 0 0 0 0 0 0 
                      0 0 0 0 0 0 0 0 0 0 0 
                       0 0 0 0 0 0 0 0 0 0 0 
                        0 0 0 0 0 0 0 0 0 0 0 
                         0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        bridgeFinder = BridgeDefender(tiles, Colour.RED)
        ans = bridgeFinder.task(Colour.RED)
        self.assertEqual(ans, (4, 6))

    def test2(self):
        board_str = (
            """0 0 0 0 0 0 0 0 0 0 0 
                0 0 0 0 0 0 0 0 0 0 0 
                 0 0 0 0 0 0 0 0 0 0 0 
                  0 0 0 0 0 0 0 0 0 0 0 
                   0 0 0 0 0 0 B R 0 0 0 
                    0 0 0 0 0 R 0 0 0 0 0 
                     0 0 0 0 0 0 0 0 0 0 0 
                      0 0 0 0 0 0 0 0 0 0 0 
                       0 0 0 0 0 0 0 0 0 0 0 
                        0 0 0 0 0 0 0 0 0 0 0 
                         0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        bridgeFinder = BridgeDefender(tiles, Colour.RED)
        ans = bridgeFinder.task(Colour.RED)
        self.assertEqual(ans, (5, 6))

    def test3(self):
        board_str = (
            """0 0 0 0 0 0 0 0 0 0 0 
                0 0 0 0 0 0 0 0 0 0 0 
                 0 0 0 0 0 0 0 0 0 0 0 
                  0 0 0 0 0 0 0 0 0 0 0 
                   0 0 0 0 0 0 0 0 0 0 0 
                    0 0 0 0 0 R 0 0 0 0 0 
                     0 0 0 0 0 B 0 0 0 0 0 
                      0 0 0 0 R 0 0 0 0 0 0 
                       0 0 0 0 0 0 0 0 0 0 0 
                        0 0 0 0 0 0 0 0 0 0 0 
                         0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        bridgeFinder = BridgeDefender(tiles, Colour.RED)
        ans = bridgeFinder.task(Colour.RED)
        self.assertEqual(ans, (6, 4))

    def test10(self):
        board_str = (
            """0 0 0 0 0 0 0 0 0 0 0 
                0 0 0 0 0 0 0 0 0 0 0 
                 0 0 0 0 0 0 0 0 0 0 0 
                  0 0 0 0 0 0 0 0 0 0 0 
                   0 0 0 0 0 0 0 R 0 0 0 
                    0 0 0 0 0 R 0 0 0 0 0 
                     0 0 0 0 0 0 0 0 0 0 0 
                      0 0 0 0 0 0 0 0 0 0 0 
                       0 0 0 0 0 0 0 0 0 0 0 
                        0 0 0 0 0 0 0 0 0 0 0 
                         0 0 0 0 0 0 0 0 0 0 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)

        tiles = [[tile.colour for tile in row] for row in board.tiles]
        bridgeFinder = BridgeDefender(tiles, Colour.RED)
        ans = bridgeFinder.task(Colour.RED)
        self.assertEqual(ans, None)


if __name__ == "__main__":
    unittest.main()
