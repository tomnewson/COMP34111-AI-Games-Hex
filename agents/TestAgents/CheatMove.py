from src.Move import Move
from src.Board import Board


class CheatMove(Move):

    def is_valid_move(self, turn: int, board: Board) -> bool:
        return True
