from src.Colour import Colour

class Cell:
    parent: None
    colour: list[list[Colour | None]]
    x: int
    y: int
    virtual_parents: tuple[tuple[int, int], tuple[int, int]]
    visited: bool


    def __init__(self, colour: list[list[Colour | None]], x, y, parent = None, virtual_parents = None):
        self.parent = parent
        self.virtual_parents = virtual_parents
        self.colour = colour
        self.x = x
        self.y = y
        self.visited = False

class ChainFinder:
    tiles: list[list[Cell]]
    player_colour: Colour

    def __init__(self, tiles, colour):
        self.tiles = [[Cell(tile, i, j) for j, tile in enumerate(row)] for i, row in enumerate(tiles)]
        self.player_colour = colour

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        """
        Returns a list of valid neighbouring nodes for a given node.
        """
        neighbour_offsets = [
            (-1, 0), (-1, 1),(0, 1),(1, 0), (1, -1),(0, -1),

        ]

        neighbours = []

        for dx, dy in neighbour_offsets:
            nx, ny = cell.x + dx, cell.y + dy
            if self.is_within_bounds((nx, ny)):
                neighbours.append(self.tiles[nx][ny])

        return neighbours
    
    def check_chain_finishes(self,cell, include_virtuals):
        # RED finishes if it reaches the bottom row
        if cell.colour == Colour.RED:
            if cell.x == 10:
                return True
            if not include_virtuals: return False
            # Check "virtual finish" from the second-to-last row
            if cell.x == 9 and cell.y + 1 < 11:
                if (self.tiles[cell.x + 1][cell.y].colour is None and
                    self.tiles[cell.x + 1][cell.y + 1].colour is None):
                    return True

        # BLUE finishes if it reaches the rightmost column
        if cell.colour == Colour.BLUE:
            if cell.y == 10:
                return True
            if not include_virtuals: return False
            # Check "virtual finish" from the second-to-last column
            if cell.y == 9 and cell.x + 1 < 11:
                if (self.tiles[cell.x][cell.y + 1].colour is None and
                    self.tiles[cell.x + 1][cell.y + 1].colour is None):
                    return True

        return False

    def reconstruct_virtual_pairs(self, leaf):
        ## check virtual kids from row/col  9 
        virtual_pairs = []

        if leaf.colour == Colour.RED and leaf.x == 9:
            virtual_pairs.append(((10,leaf.y),(10, leaf.y + 1)))

        if leaf.colour == Colour.BLUE and leaf.y == 9:
            virtual_pairs.append(((leaf.x -1,10),(leaf.x,10)))

        while leaf:
            if leaf.virtual_parents:
                virtual_pairs.append(leaf.virtual_parents)
            leaf = leaf.parent
        return virtual_pairs

    def search(self, include_virtuals = True) -> tuple[bool, list[tuple[tuple[int, int], tuple[int, int]]]]:
        stack = []

        starting_cells = self.starting_cells(include_virtuals)

        # Initialize the stack
        for cell in starting_cells:
            stack.append(cell)
        while stack:
            current_cell = stack.pop()

            #check visited
            if (current_cell.visited):
                continue

            current_cell.visited = True

            #check end of chain
            if (self.check_chain_finishes(current_cell, include_virtuals)):
                if include_virtuals:
                    return (True, self.reconstruct_virtual_pairs(current_cell))
                return (True, None)
            #search for linked neighbour
            cell_neighbours = self.get_neighbours(current_cell)
            for neighbour in cell_neighbours:
                if not neighbour.visited and neighbour.colour == current_cell.colour:
                    neighbour.parent = current_cell
                    stack.append(neighbour)

            if not include_virtuals:
                continue

            num_neighbours = len(cell_neighbours)
            for i in range(num_neighbours):
                first_neighbour = cell_neighbours[i]
                second_neighbour = cell_neighbours[0] if i == num_neighbours - 1 else cell_neighbours[i+1]

                if first_neighbour.colour is None and second_neighbour.colour is None:
                    first_neighbour_neighbours = set(self.get_neighbours(first_neighbour))
                    second_neighbour_neighbours = set(self.get_neighbours(second_neighbour))
                    virtual_neighbours = (first_neighbour_neighbours).intersection(second_neighbour_neighbours)

                    for virtual_neighbour in virtual_neighbours:
                        if (not virtual_neighbour.visited) and (virtual_neighbour.colour == current_cell.colour):
                            # VIRTUAL CONNECTION FOUND!!!!
                            virtual_neighbour.virtual_parents = ((first_neighbour.x, first_neighbour.y), (second_neighbour.x, second_neighbour.y))
                            virtual_neighbour.parent = current_cell
                            stack.append(virtual_neighbour)

        return (False, None)

    def starting_cells(self, include_virtuals):
        #RED: TOP TO BOTTOM
        if self.player_colour == Colour.RED:
            red_top_row_starts = [cell for cell in self.tiles[0] if cell.colour == self.player_colour]
            if not include_virtuals: 
                return red_top_row_starts
            red_second_row_starts = [
                    cell for y, cell in enumerate(self.tiles[1])
                    if cell.colour == self.player_colour
                    and y + 1 < 11
                    and self.tiles[0][y].colour is None
                    and self.tiles[0][y+1].colour is None
                ]   
            for cell in red_second_row_starts:
                cell.virtual_parents = ((0,cell.y),(0,cell.y + 1))
            
            return red_top_row_starts + red_second_row_starts
        # BLUE: LEFT TO RIGHT
        blue_top_col_starts = [row[0] for row in self.tiles if row[0].colour == self.player_colour]
        if not include_virtuals: 
            return blue_top_col_starts
        blue_second_column_starts = [
            row[1] for x, row in enumerate(self.tiles)
            if row[1].colour == self.player_colour
            and x + 1 < 11
            and self.tiles[x][0].colour is None
            and self.tiles[x+1][0].colour is None
        ]

        for cell in blue_second_column_starts:
            cell.virtual_parents = ((cell.x,0),(cell.x + 1,0))

        return blue_top_col_starts + blue_second_column_starts

    def is_within_bounds(self, node: tuple[int, int]) -> bool:
        """
        Checks if a node is within the bounds of the board.
        """
        x, y = node
        return 0 <= x < 11 and 0 <= y < 11
