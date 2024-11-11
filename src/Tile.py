from dataclasses import dataclass

from src.Colour import Colour


@dataclass
class Tile:
    """The class representation of a tile on a board of Hex."""

    # number of neighbours a tile has
    NEIGHBOUR_COUNT = 6

    # relative positions of neighbours, clockwise from top left
    I_DISPLACEMENTS = [-1, -1, 0, 1, 1, 0]
    J_DISPLACEMENTS = [0, 1, 1, 0, -1, -1]

    _x: int
    _y: int
    _colour: Colour = None
    _visited: bool = False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    def visit(self):
        self._visited = True

    def is_visited(self):
        return self._visited

    def clear_visit(self):
        self._visited = False
