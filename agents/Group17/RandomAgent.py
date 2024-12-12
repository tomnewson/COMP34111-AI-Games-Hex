from random import choice
from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

from agents.TestAgents.utils import make_valid_move

class RandomAgent(AgentBase):

    _board_size: int = 11

    def __init__(self, colour: Colour):
        super().__init__(colour)


    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        if turn == 2:
            return Move(-1, -1)
        else:
            moves_row = choice(board.tiles)
            tile = choice(moves_row)
            
            while tile.colour is not None:
                moves_row = choice(board.tiles)
                tile = choice(moves_row)
            
            return Move(tile.x, tile.y)
            
            
