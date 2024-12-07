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


    def check_chain_finishes(self):
        if self.colour == Colour.RED and self.x == 10:  # last row for RED
            # We've reached the bottom. Reconstruct path and return it.
            return True

        if self.colour  == Colour.BLUE and self.y == 10: # last column for BLUE
            # We've reached the right side. Reconstruct path and return it.
            return True

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
    
    def reconstruct_virtual_pairs(self, leaf):
        virtual_pairs = []
        while leaf:
            if leaf.virtual_parents:
                virtual_pairs.append(leaf.virtual_parents)
            leaf = leaf.parent
        print(virtual_pairs)
        return virtual_pairs

    def search(self) -> tuple[bool, list[tuple[tuple[int, int], tuple[int, int]]]]:
        stack = []

        starting_cells = self.starting_cells()

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
            if (current_cell.check_chain_finishes()):
                print("ending...")
                return (True, self.reconstruct_virtual_pairs(current_cell))

            #search for linked neighbour
            cell_neighbours = self.get_neighbours(current_cell)
            for neighbour in cell_neighbours:
                if not neighbour.visited and neighbour.colour == current_cell.colour:
                    neighbour.parent = current_cell
                    stack.append(neighbour)
            
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
    
    def starting_cells(self):
        if self.player_colour == Colour.RED:
            # Start from the top row and aim for the bottom row
            return [cell for cell in self.tiles[0] if cell.colour == self.player_colour]
        # Start from the left column and aim for the right column
        return [row[0] for row in self.tiles if row[0].colour == self.player_colour]

    def is_within_bounds(self, node: tuple[int, int]) -> bool:
        """
        Checks if a node is within the bounds of the board.
        """
        x, y = node
        return 0 <= x < 11 and 0 <= y < 11
