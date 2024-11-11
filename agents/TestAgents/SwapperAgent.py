from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

from agents.TestAgents.utils import make_valid_move

class SwapperAgent(AgentBase):

    _board_size: int = 11

    def __init__(self, colour: Colour):
        super().__init__(colour)


    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        # check that you can't swap on turns later than turn 2
        if turn == 1:
            return make_valid_move(board)
        else:
            return Move(-1, -1)
