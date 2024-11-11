import unittest

from src.Board import Board
from src.Move import Move

# NOTE: LLM generated tests not checked by human


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = Board(11)

    def test_move_string_representation(self):
        move = Move(2, 3)
        self.assertEqual(str(move), "(x=2, y=3)")

    def test_swap_move_string_representation(self):
        move = Move(-1, -1)
        self.assertEqual(str(move), "SWAP()")

    def test_move_properties(self):
        move = Move(4, 7)
        self.assertEqual(move.x, 4)
        self.assertEqual(move.y, 7)


if __name__ == "__main__":
    unittest.main()
