from src.Colour import Colour

def has_winning_chain(tiles: list[list[Colour | None]], player_colour: Colour) -> list[tuple[int,int]] | None:
    """
    Performs a DFS search to determine if there is a winning chain for the given player.
    The chain can be a direct chain of tiles of the same colour or a virtual connection.

    Returns:
        list of (x,y) positions forming the winning chain if found, otherwise None.
    """
    visited = set()
    stack = []
    parent = {}  # Map each node to its parent for path reconstruction

    # Determine starting positions based on player colour
    if player_colour == Colour.RED:
        # Start from the top row and aim for the bottom row
        starts = [(0, c) for c in range(11) if tiles[0][c] == player_colour]
    elif player_colour == Colour.BLUE:
        # Start from the left column and aim for the right column
        starts = [(r, 0) for r in range(11) if tiles[r][0] == player_colour]
    else:
        raise ValueError("Invalid player colour.")

    # Initialize the stack
    for s in starts:
        stack.append(s)
        parent[s] = None

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        x, y = current

        # Check if the current tile meets the win condition
        if player_colour == Colour.RED and x == 10:  # last row for RED
            # We've reached the bottom. Reconstruct path and return it.
            return reconstruct_path(parent, current)

        if player_colour == Colour.BLUE and y == 10: # last column for BLUE
            # We've reached the right side. Reconstruct path and return it.
            return reconstruct_path(parent, current)

        # Explore neighbours
        for neighbour in get_neighbours(current):
            nx, ny = neighbour

            if neighbour in visited:
                continue

            # Direct connection (same colour)
            if tiles[nx][ny] == player_colour:
                parent[neighbour] = current
                stack.append(neighbour)

            # Virtual connection: Check if this empty node could lead to a path
            elif tiles[nx][ny] is None:
                # Check if there's a tile of player_colour adjacent to this empty cell
                # that forms a valid virtual connection
                for intermediate in get_neighbours(neighbour):
                    ix, iy = intermediate
                    if tiles[ix][iy] == player_colour and has_virtual_connection(tiles, current, intermediate):
                        parent[neighbour] = current
                        stack.append(neighbour)
                        break

    return None


def get_neighbours(node: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of valid neighbouring nodes for a given node.
    """
    x, y = node
    neighbour_offsets = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, 1), (1, -1),
    ]
    neighbours = []

    for dx, dy in neighbour_offsets:
        nx, ny = x + dx, y + dy
        if is_within_bounds((nx, ny)):
            neighbours.append((nx, ny))

    return neighbours


def is_within_bounds(node: tuple[int, int]) -> bool:
    """
    Checks if a node is within the bounds of the board.
    """
    x, y = node
    return 0 <= x < 11 and 0 <= y < 11


def has_virtual_connection(tiles: list[list[Colour | None]], n1: tuple[int, int], n2: tuple[int, int]) -> list[tuple[int,int]] | None:
    """
    Determines if there is a virtual connection between two nodes (n1 and n2) on the board.
    A virtual connection is simplified here as having the same colour and having exactly two shared empty neighbours.

    Adjust logic if this is too permissive or causing false positives.
    """
    x1, y1 = n1
    x2, y2 = n2

    # Both must be same colour and not None
    if tiles[x1][y1] is None or tiles[x2][y2] is None:
        return False
    if tiles[x1][y1] != tiles[x2][y2]:
        return False

    neighbours_n1 = set(get_neighbours(n1))
    neighbours_n2 = set(get_neighbours(n2))
    shared_neighbours = neighbours_n1.intersection(neighbours_n2)

    # Check for exactly two distinct unoccupied connecting cells
    connecting_cells = [cell for cell in shared_neighbours if tiles[cell[0]][cell[1]] is None]

    return len(connecting_cells) == 2


def reconstruct_path(parent: dict, end_node: tuple[int,int]) -> list[tuple[int,int]]:
    """
    Reconstructs the path from the start node to the end node using the parent dictionary.
    """
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path
