from src.Colour import Colour

RED = "\033[31m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"


class Cell:
    parent: None
    colour: list[list[Colour | None]]
    x: int
    y: int
    virtual_parents: tuple[tuple[int, int], tuple[int, int]]
    visited: bool

    def __init__(
        self, colour: list[list[Colour | None]], x, y, parent=None, virtual_parents=None
    ):
        self.parent = parent
        self.virtual_parents = virtual_parents
        self.colour = colour
        self.x = x
        self.y = y
        self.visited = False


class BridgeDefender:
    tiles: list[list[Cell]]

    def __init__(self, tiles, colour):
        self.tiles = [
            [Cell(tile, i, j) for j, tile in enumerate(row)]
            for i, row in enumerate(tiles)
        ]
        self.playerColour = colour

    def task(self, playerColour):
        return self.findBridges(playerColour)

    def findBridges(self, playerColour):
        print(
            f"{RED if playerColour == Colour.RED else BLUE}Finding bridges for {playerColour}...{RESET}"
        )
        bridges = []
        opponentColour = Colour.RED if playerColour == Colour.BLUE else Colour.BLUE
        bridges.append("test")
        # 0 0 0 0 0 X 0 0 0
        #  0 0 0 X 0 0 X 0 0
        #   0 0 0 0 S 0 0 0 0
        #    0 0 X 0 0 X 0 0 0
        #     0 0 0 X 0 0 0 0 0
        bridgeOffsets = [(1, -2), (2, -1), (1, 1), (-1, 2), (-2, 1), (-1, -1)]

        midOffsets = {
            (1, -2): [(0, -1), (1, -1)],
            (2, -1): [(1, -1), (1, 0)],
            (1, 1): [(1, 0), (0, 1)],
            (-1, 2): [(0, 1), (-1, 1)],
            (-2, 1): [(-1, 1), (-1, 0)],
            (-1, -1): [(-1, 0), (0, -1)],
        }
        for row in self.tiles:
            for cell in row:
                if cell.colour == playerColour:
                    cell.visited = True
                    for dx, dy in bridgeOffsets:
                        nx, ny = cell.x + dx, cell.y + dy
                        # possible bridge
                        if (
                            self.isWithinBounds((nx, ny))
                            and self.tiles[nx][ny].colour == playerColour
                            and not self.tiles[nx][ny].visited
                        ):
                            print(
                                f"Potential Bridge Found! ({cell.x},{cell.y})({nx},{ny})"
                            )
                            (mx0, my0), (mx1, my1) = midOffsets[(dx, dy)]
                            midx0, midy0 = cell.x + mx0, cell.y + my0
                            midx1, midy1 = cell.x + mx1, cell.y + my1

                            tile0 = self.tiles[midx0][midy0]
                            tile1 = self.tiles[midx1][midy1]

                            conditions = [
                                (tile0.colour == opponentColour and tile1.colour is None, (midx1, midy1)),
                                (tile0.colour is None and tile1.colour == opponentColour, (midx0, midy0))
                            ]

                            # Check conditions
                            for condition, result in conditions:
                                if condition:
                                    return result

        return None

    def isWithinBounds(self, node: tuple[int, int]) -> bool:
        """
        Checks if a node is within the bounds of the board.
        """
        x, y = node
        return 0 <= x < 11 and 0 <= y < 11
