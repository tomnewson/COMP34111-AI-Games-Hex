import unittest

from src.Board import Board
from src.Colour import Colour
from src.Move import Move
from agents.Group17.GoodAgent import GoodAgent

class TestAgent(unittest.TestCase):
    def test_get_neighbours_middle(self):
        agent = GoodAgent(Colour.RED)
        position = (4, 4)
        expected = [(3, 4), (3, 5), (4, 5), (5, 4), (5, 3), (4, 3)]
        actual = agent.get_neighbours(position)
        self.assertCountEqual(actual, expected)

    def test_get_neighbours_left_edge(self):
        agent = GoodAgent(Colour.RED)
        position = (4, 0)
        expected = [(3, 0), (3, 1), (4, 1), (5, 0)]
        actual = agent.get_neighbours(position)
        self.assertCountEqual(actual, expected)

    def test_get_neighbours_near_right_edge(self):
        agent = GoodAgent(Colour.RED)
        position = (6, 9)
        expected = [(5, 9), (5, 10), (6, 10), (7, 9), (7, 8), (6, 8)]
        actual = agent.get_neighbours(position)
        self.assertCountEqual(actual, expected)

    def test_get_neighbours_bottom_right(self):
        agent = GoodAgent(Colour.RED)
        position = (10, 10)
        expected = [(9, 10), (10, 9)]
        actual = agent.get_neighbours(position)
        self.assertCountEqual(actual, expected)

    def test_find_winning_move_from_edge(self):
        board_str = (
        """R R R R R R B R B R R
            R R R R R R R R R R R
             B R B R R B R R B B B
              R R B B 0 0 0 B B 0 B
               B 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0
                 0 R 0 0 B 0 0 0 0 B 0
                  0 B 0 0 0 0 0 B B 0 0
                   0 0 B B B B B 0 0 0 0
                    B B 0 0 0 0 0 0 0 0 0
                     0 0 0 0 0 0 0 0 0 B 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        state = [[tile.colour for tile in row] for row in board.tiles]
        self.assertEqual(board.size, 11)
        agent = GoodAgent(Colour.BLUE)
        position = (6,9)
        expected_moves = ((5,10), (6,10))

        actual_move = agent.find_winning_move_from(state, position, [])
        self.assertIsNotNone(actual_move)
        self.assertIn(actual_move, expected_moves)

    def test_e2e_make_winning_move_right_edge(self):
        board_str = (
        """R R R R R R B R B R R
            R R R R R R R R R R R
             B R B R R B R R B B B
              R R B B 0 0 0 B B 0 B
               B 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0
                 0 R 0 0 B 0 0 0 0 B 0
                  0 B 0 0 0 0 0 B B 0 0
                   0 0 B B B B B 0 0 0 0
                    B B 0 0 0 0 0 0 0 0 0
                     0 0 0 0 0 0 0 0 0 B 0"""
        )
        board = Board.from_string(board_str, board_size=11)
        self.assertEqual(board.size, 11)
        agent = GoodAgent(Colour.BLUE)
        expected_moves = (Move(5,10), Move(6,10))
        actual_move = agent.make_move(57, board, Move(3,1))
        self.assertIn(actual_move, expected_moves)

if __name__ == "__main__":
    unittest.main()
