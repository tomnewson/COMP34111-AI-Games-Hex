from random import choice
import time
import math
import copy

from src.AgentBase import AgentBase
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
        for col in range(B.size):
            if B.tiles[0][col].colour == player_colour:
                stack.append((0, col))
    elif player_colour == Colour.BLUE:
        # Start from the left column and aim for the right column
        for row in range(B.size):
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
        if player_colour == Colour.RED and x == B.size - 1:
            return True  # Reached the bottom row
        if player_colour == Colour.BLUE and y == B.size - 1:
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
    return 0 <= x < B.size and 0 <= y < B.size


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



def winvalue(B: Board, player: Colour):
    """
    Computes the winvalue of a given board configuration B for player.

    Args:
        B: The board configuration (a data structure representing the game state).
        player: The current player to move.

    Returns:
        tuple: (v, X) where v is 1/-1 if the player wins/loses and X is a win-set.
    """
    # Check if the current player has a winning chain
    if has_winning_chain(B, player):
        return (+1, set())

    opponent = get_opponent(player)
    # Check if the opponent has a winning chain
    if has_winning_chain(B, opponent):
        return (-1, set())

    # Initialize W (the win-set) and M (the must-play cells)
    W = set()
    M = get_unoccupied_cells(B)

    # Iterate while there are still cells to consider
    while M:
        cell = M.pop()

        # Simulate the board after placing the player's stone in cell m
        B_next = make_move(B, cell, player)

        # Recursive call to evaluate the opponent's response
        v, S = winvalue(B_next, opponent)

        if v == -1:
            return (+1, S.union({cell}))

        W = W.union(S)
        M = M.intersection(S)

    return (-1, W)


def get_opponent(player):
    if player == Colour.RED:
        return Colour.BLUE
    return Colour.RED

def get_unoccupied_cells(B: Board) -> set[tuple[int, int]]:
    unoccupied_cells = set()
    for row in range(B.size):
        for col in range(B.size):
            if B.tiles[row][col].colour is None:  # Check if the tile is unoccupied
                unoccupied_cells.add((row, col))

    return unoccupied_cells

def make_move(B: Board, cell: tuple[int, int], player: Colour):
    x, y = cell
    B.tiles[x][y].colour = player
    return B


def select_best_move(B: Board, player: Colour) -> Move:
    """
    Selects the best move for the agent using the winvalue algorithm.

    Args:
        B: The current board configuration.
        player: The player's colour.

    Returns:
        Move: The best move for the player.
    """
    unoccupied_cells = get_unoccupied_cells(B)
    best_move = None
    best_value = -math.inf
    smallest_win_set_size = math.inf

    for cell in unoccupied_cells:
        # Create a deep copy of the board to simulate the move
        simulated_board = copy.deepcopy(B)
        make_move(simulated_board, cell, player)

        # Evaluate the board state after the simulated move
        value, win_set = winvalue(simulated_board, get_opponent(player))

        # If this move guarantees a win, return it immediately
        if value == +1:
            return Move(cell[0], cell[1])

        # If the value is better, prioritize this move
        if value > best_value:
            best_value = value
            best_move = cell
            smallest_win_set_size = len(win_set)

        # If the value is the same, prioritize the smaller win-set
        elif value == best_value and len(win_set) < smallest_win_set_size:
            best_move = cell
            smallest_win_set_size = len(win_set)

    if best_move is None:
        print("none")
        # If no winning move is found, choose a random cell as a fallback
        return -1

    return Move(best_move[0], best_move[1])


class MyAgent(AgentBase):
    """This class describes the default Hex agent. It will randomly send a
    valid move at each turn, and it will choose to swap with a 50% chance.

    The class inherits from AgentBase, which is an abstract class.
    The AgentBase contains the colour property which you can use to get the agent's colour.
    You must implement the make_move method to make the agent functional.
    You CANNOT modify the AgentBase class, otherwise your agent might not function.
    """

    _choices: list[Move]
    _board_size: int = 11
    _time_limit: float = 5 # seconds per move
    EXPLORATION_CONSTANT = 2

    class Node:
        """Node class for MCTS"""
        board: Board
        action: Move | None
        actions: list[Move]
        parent: None
        children: None
        total_score: int
        visits: int
        our_turn: bool

        def __init__(self, board: Board, actions: list[Move], our_turn: bool, parent = None, action = None):
            self.board = board
            self.actions = actions
            self.parent = parent
            self.action = action
            self.children = []
            self.total_score = 0
            self.visits = 0
            self.our_turn = our_turn

        def add_child(self, child):
            """Expand node"""
            self.children.append(child)

        # Call UCT for each child node in a function to evaluate
        # which one is higher
        def UCT(self, risk):
            """Upper Confidence Bound for Trees"""
            if self.visits == 0:
                return math.inf

            average_value = self.total_score / self.visits
            exploration = risk * (math.sqrt(math.log(self.parent.visits) / self.visits))

            return average_value + exploration

        def best_child(self, risk = 2):
            """Return child with highest UCT value
            will only be called if node has children
            """
            best_child = (None, -math.inf)

            for child in self.children:
                if child.visits == 0:
                    return child
                uct = child.UCT(risk)
                if uct > best_child[1]:
                    best_child = (child, uct)
            return best_child[0]

        def expand(self, colours: list[Colour]):
            """MCTS Expansion phase
            what are the node's actions?
            for each action, create a new node with the resulting state
            add the new node as a child of the current node
            """
            for move in self.actions:
                new_actions = self.actions.copy()
                new_actions.remove(move)
                new_board = copy.deepcopy(self.board)
                colour = colours[0] if self.our_turn else colours[1]
                new_board.set_tile_colour(move.x, move.y, colour)

                self.add_child(
                    MyAgent.Node(
                        board=new_board,
                        our_turn=not self.our_turn,
                        parent=self,
                        actions=new_actions,
                        action = move,
                    )
                )

    def __init__(self, colour: Colour):
        super().__init__(colour)
        self._choices = [
            Move(i, j) for i in range(self._board_size) for j in range(self._board_size)
        ]

    def select_node(self, node: Node):
        """MCTS Selection phase
        Call best_child() with exploration constant (risk)
        Repeat until leaf node is reached
        Return selection
        """
        while True:
            if not node.children:
                return node # return leaf node
            node = node.best_child(self.EXPLORATION_CONSTANT)

    def get_result(self, board: Board):
        if board.has_ended(self.colour):
            return 1
        return -1

    def playout(self, node: Node):
        """MCTS Playout phase
        Apply policy until move is terminal
        Backpropagate result
        Return result
        """
        available_actions = node.actions.copy()
        shuffle(available_actions)
        final_board = self.play(copy.deepcopy(node.board), available_actions, not node.our_turn)
        result = self.get_result(final_board)
        self.backpropagate(node, result)

    def play(self, board: Board, available_actions: list[Move], our_turn: bool):
        """Play until no actions
        Return board"""
        if not available_actions:
            return board

        colour = self.colour if our_turn else self.opp_colour()
        move = available_actions.pop()

        board.set_tile_colour(move.x, move.y, colour)
        return self.play(board, available_actions, not our_turn)


    def backpropagate(self, node: Node, result: float):
        """MCTS Backpropagation phase"""
        node.visits += 1
        node.total_score += result

        if node.parent:
            self.backpropagate(node.parent, result)

    def mcts(self, board: Board, start_time: float):
        """Monte Carlo Tree Search
        Each node in tree is a Board"""
        root = MyAgent.Node(board, actions=self._choices, our_turn=True)
        sims = 0
        while True:
            # time_elapsed = time.time() - start_time
            # if time_elapsed >= self._time_limit:
            #     break
            if sims >= 100:
                break
            sims += 1

            # Selection
            leaf = self.select_node(root)

            if leaf.visits > 0 and leaf.actions:
                # Expansion
                leaf.expand([self.colour, self.opp_colour()])
                leaf = leaf.children[0]
            # Play/Rollout
            # do we want to playout from terminal nodes?
            self.playout(leaf)

        if root.children:
            move = root.best_child(0)
            print(f"move: {move.action}, value: {move.total_score} / {move.visits}, total simulations: {sims} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return move.action
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nfailed, picking randomly\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        return self._pick_random_move(self._choices)

    def _pick_random_move(self, choices):
        """Pick a random move from the list of choices"""
        return choice(choices)

    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        """The game engine will call this method to request a move from the agent.
        If the agent is to make the first move, opp_move will be None.
        If the opponent has made a move, opp_move will contain the opponent's move.
        If the opponent has made a swap move, opp_move will contain a Move object with x=-1 and y=-1,
        the game engine will also change your colour to the opponent colour.

        Args:
            turn (int): The current turn
            board (Board): The current board state
            opp_move (Move | None): The opponent's last move

        Returns:
            Move: The agent's move
        """

        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove(opp_move)

        # ALWAYS SWAP
        if turn == 2:
            return Move(-1, -1)

        # move = self.mcts(board, time.time())
        sim_board = copy.deepcopy(board)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(board.size)
        move = select_best_move(board, self.colour)
        if move == -1:
            move = self.mcts(board, time.time())
        self._choices.remove(move)
        return move
