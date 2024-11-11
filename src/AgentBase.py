import inspect
from abc import ABC, abstractmethod

from src.Board import Board
from src.Colour import Colour
from src.Move import Move


class AgentBase(ABC):
    """This class describes the base agent class. All agents should inherit from this class."""

    @abstractmethod
    def __init__(self, colour: Colour):
        self._colour = colour

    @abstractmethod
    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        """Makes a move based on the current board state."""
        pass

    @property
    def colour(self) -> Colour:
        return self._colour

    @colour.setter
    def colour(self, colour: Colour):
        self._colour = colour

    def opp_colour(self) -> Colour:
        """Returns the char representation of the colour opposite to the
        current one.
        """

        if self._colour == Colour.RED:
            return Colour.BLUE
        elif self._colour == Colour.BLUE:
            return Colour.RED
        else:
            raise ValueError(f"Invalid colour: {self._colour}")

    def __hash__(self) -> int:
        return hash(inspect.getsource(self.__class__))
