from src.Board import Board
from src.Move import Move


def make_valid_move(board: Board) -> Move:
    for i in range(board.size):
        for j in range(board.size):
            t = board.tiles[i][j]
            if t.colour is None:
                return Move(i, j)
