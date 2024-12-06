from src.Board import Board
from src.Colour import Colour
from src.Move import Move



def has_winning_chain(B: Board, player_colour: Colour) -> bool:
    """
    Performs a DFS search to determine if there is a winning chain for the given player.
    The chain can be a direct chain of tiles of the same colour or a virtual connection.

    Args:
        B: Board object representing the current Hex board state.
        player_colour: Colour of the player to check for a winning chain.

    Returns:
        bool: True if there is a winning chain, False otherwise.
    """
    visited = set()
    stack = []

    # Determine starting edge based on player colour
    if player_colour == Colour.RED:
        # Start from the top row and aim for the bottom row
        for col in range(0,11):
            if B.tiles[0][col].colour == player_colour:
                stack.append((0, col))
    elif player_colour == Colour.BLUE:
        # Start from the left column and aim for the right column
        for row in range(0,11):
            if B.tiles[row][0].colour == player_colour:
                stack.append((row, 0))
    else:
        raise ValueError("Invalid player colour.")

    # Perform DFS
    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        x, y = current

        # Check if the current tile meets the win condition
        if player_colour == Colour.RED and x == 11 - 1:
            return True  # Reached the bottom row
        if player_colour == Colour.BLUE and y == 11 - 1:
            return True  # Reached the right column

        # Get all neighbors
        neighbors = get_neighbors(B, current)

        for neighbor in neighbors:
            nx, ny = neighbor

            # Check direct connection (same colour)
            if B.tiles[nx][ny].colour == player_colour and neighbor not in visited:
                stack.append(neighbor)

            # Check virtual connection
            elif B.tiles[nx][ny].colour is None and neighbor not in visited:
                # Look for a virtual connection
                for intermediate in get_neighbors(B, neighbor):
                    ix, iy = intermediate
                    if (
                        B.tiles[ix][iy].colour == player_colour
                        and has_virtual_connection(B, current, intermediate)
                    ):
                        stack.append(neighbor)
    return False


def get_neighbors(B: Board, node: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of valid neighboring nodes for a given node.
    """
    x, y = node
    neighbor_offsets = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Standard hex neighbors
        (-1, 1), (1, -1),
    ]
    neighbors = []

    for dx, dy in neighbor_offsets:
        nx, ny = x + dx, y + dy
        if is_within_bounds(B, (nx, ny)):  # Ensure the neighbor is within bounds
            neighbors.append((nx, ny))

    return neighbors


def is_within_bounds(B: Board, node: tuple[int, int]) -> bool:
    """
    Checks if a node is within the bounds of the board.
    """
    x, y = node
    return 0 <= x < 11 and 0 <= y < 11


def has_virtual_connection(B: Board, n1: tuple[int, int], n2: tuple[int, int]) -> bool:
    """
    Determines if there is a virtual connection between two nodes (n1 and n2) on the board.
    A virtual connection exists if:
    1. n1 and n2 are the same colour.
    2. There are two distinct cells connecting n1 and n2, and both are unoccupied.

    Args:
        B: Board object representing the Hex board.
        n1: Tuple representing the coordinates of the first node (row, col).
        n2: Tuple representing the coordinates of the second node (row, col).

    Returns:
        bool: True if there is a virtual connection, False otherwise.
    """
    x1, y1 = n1
    x2, y2 = n2

    # Check if n1 and n2 are the same colour
    if B.tiles[x1][y1].colour != B.tiles[x2][y2].colour:
        return False

    # Both tiles must have the same colour
    if B.tiles[x1][y1].colour is None:
        return False

    # Find the shared neighbors of n1 and n2
    neighbors_n1 = get_neighbors(B, n1)
    neighbors_n2 = get_neighbors(B, n2)

    # Check for two distinct unoccupied connecting cells
    connecting_cells = []
    for neighbor in neighbors_n1:
        if neighbor in neighbors_n2:
            nx, ny = neighbor
            if B.tiles[nx][ny].colour is None:  # Cell is unoccupied
                connecting_cells.append(neighbor)

    # A virtual connection exists if there are exactly two unoccupied connecting cells
    return len(connecting_cells) == 2

