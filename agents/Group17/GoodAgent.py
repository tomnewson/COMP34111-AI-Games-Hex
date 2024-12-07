from random import choice, shuffle
from time import time
import math

from agents.Group17.haswin import has_winning_chain
from agents.Group17.windetect import select_best_move
from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move
from src.Tile import Tile


class Node:
    children = None # set in expansion
    parent: None # never changes

    state: list[list[Colour | None]] # never changes
    prev_action: None | Move # never changes
    available_actions: list[Move] # never changes

    visits: int = 0 # increases in backpropagation
    value: int = 0# increases in backpropagation
    our_turn: bool # never changes

    def __init__(self, state: list[list[Colour | None]], available_actions: list[Move], our_turn: bool, parent = None, prev_action = None):
        self.parent = parent
        self.state = state
        self.available_actions = available_actions
        self.our_turn = our_turn
        self.prev_action = prev_action
        self.children = []

    def UCT(self, risk, parent_visits):
        if self.visits == 0:
            return math.inf
        return self.value / self.visits + risk * math.sqrt(math.log(parent_visits) / self.visits)


class GoodAgent(AgentBase):
    _choices: list[Move]
    _board_size: int = 11
    _time_limit: int = 5 # seconds per move
    _max_iterations: int = 10_000
    EXPLORATION_CONSTANT = 2
    _parent_node_visits: int
    winning_chain = None

    def __init__(self, colour: Colour):
        super().__init__(colour)
        self._choices = [
            Move(i, j) for i in range(self._board_size) for j in range(self._board_size)
        ]

    def selection(self, node: Node):
        while node.children:
            node = max(node.children, key=lambda child: child.UCT(self.EXPLORATION_CONSTANT, self._parent_node_visits))
        return node

    def expansion(self, node: Node):
        # expand all children at once
        for action in node.available_actions:
            new_state = self.copy_state(node.state)
            colour = self.colour if node.our_turn else self.opp_colour()
            new_state[action.x][action.y] = colour
            new_available_actions = [a for a in node.available_actions if a != action]
            node.children.append(Node(
                state=new_state,
                available_actions=new_available_actions,
                our_turn=not node.our_turn,
                parent=node,
                prev_action=action,
            ))

    def simulation(self, node: Node):
        # play until no available actions remain
        available_actions = node.available_actions.copy()
        state = self.copy_state(node.state)
        our_turn = not node.our_turn
        shuffle(available_actions)
        while available_actions:
            action = available_actions.pop()
            state[action.x][action.y] = self.colour if our_turn else self.opp_colour()
            our_turn = not our_turn

        # if somehow the whole board gets filled without a win being detected
        tiles = [[Tile(i, j, state[i][j]) for j in range(self._board_size)] for i in range(self._board_size)]
        return self.did_i_win(tiles)

    def backpropagation(self, node: Node, win: bool):
        while node:
            node.visits += 1
            if win and not node.our_turn:
                node.value += 1
            elif not win and node.our_turn:
                node.value += 1
            node = node.parent
        self._parent_node_visits += 1

    def did_i_win(self, tiles: list[list[Tile]]) -> bool:
        """Copied from Board - Checks if the game has ended. It will attempt to find a red chain
        from top to bottom or a blue chain from left to right of the board.
        """

        if self.colour == Colour.RED:
            for idx in range(self._board_size):
                tile = tiles[0][idx]
                if not tile.is_visited() and tile.colour == Colour.RED and self.DFS_colour(0, idx, tiles):
                    return True
        else:
            for idx in range(self._board_size):
                tile = tiles[idx][0]
                if not tile.is_visited() and tile.colour == Colour.BLUE and self.DFS_colour(idx, 0, tiles):
                    return True

        return False

    def DFS_colour(self, x, y, tiles):
        """Copied from Board - A recursive DFS method that iterates through connected same-colour
        tiles until it finds a bottom tile (Red) or a right tile (Blue).
        """

        tiles[x][y].visit()

        # win conditions
        if self.colour == Colour.RED:
            if x == self._board_size - 1:
                return True
        else:
            if y == self._board_size - 1:
                return True

        # visit neighbours
        for idx in range(Tile.NEIGHBOUR_COUNT):
            x_n = x + Tile.I_DISPLACEMENTS[idx]
            y_n = y + Tile.J_DISPLACEMENTS[idx]
            if (0 <= x_n < self._board_size) and (0 <= y_n < self._board_size):
                neighbour = tiles[x_n][y_n]
                if not neighbour.is_visited() and neighbour.colour == self.colour and self.DFS_colour(x_n, y_n, tiles):
                    # Check if the recursive call found a winning path
                    return True

        # If no path found from this tile, return False
        return False

    def copy_state(self, state):
        """rows are mutable, so we need a deep copy"""
        return [list(row) for row in state]

    def mcts(self, state, available_actions, start_time):
        root = Node(
            state=state,
            available_actions=available_actions,
            our_turn=True
        )
        self._parent_node_visits = 0
        self.expansion(root)
        print(f"Setup time: {time() - start_time:.5f}s")

        iterations = 0
        selection_times = []
        expansion_times = []
        simulation_times = []
        backpropagation_times = []
        while iterations < self._max_iterations and time() - start_time < self._time_limit:
            iterations += 1
            # Selection
            selection_start_time = time()
            leaf = self.selection(root)
            selection_times.append(time() - selection_start_time)
            # Expansion
            expansion_start_time = time()
            if leaf.visits > 0 and leaf.available_actions:
                self.expansion(leaf)
                leaf = choice(leaf.children)
            expansion_times.append(time() - expansion_start_time)
            # Simulation
            simulation_start_time = time()
            win = self.simulation(leaf)
            simulation_times.append(time() - simulation_start_time)
            # Backpropagation
            backpropagation_start_time = time()
            self.backpropagation(leaf, win)
            backpropagation_times.append(time() - backpropagation_start_time)

        available_moves_str = '\t'.join(
            [f'({child.prev_action.x},{child.prev_action.y}): {child.value}/{child.visits}' for child in root.children]
        )
        print(f"""Average times after {iterations} iterations:
                Selection: {(sum(selection_times) / iterations):.5f}s
                Expansion: {(sum(expansion_times) / iterations):.5f}s
                Simulation: {(sum(simulation_times) / iterations):.5f}s
                Backpropagation: {(sum(backpropagation_times) / iterations):.5f}s

                Available Moves:
                {available_moves_str}
        """)

        node = max(root.children, key=lambda child: child.UCT(0, self._parent_node_visits))
        return node.prev_action

    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        start_time = time()

        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove(opp_move)

        # ALWAYS SWAP
        if turn == 2:
            return Move(-1, -1)

        state = [[tile.colour for tile in row] for row in board.tiles]

        # check for winning chains
        if not self.winning_chain:
            self.winning_chain = has_winning_chain(state, self.colour)
        if self.winning_chain:
            print("winning chain: ", self.winning_chain)
            for move in self.winning_chain:
                if Move(move[0], move[1]) in self._choices:
                    self._choices.remove(move)
                    print(f"winning move: {move}")
                    return move

        move = self.mcts(state, self._choices, start_time)
        self._choices.remove(move)
        return move

class AlexAgent(GoodAgent):
    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove(opp_move)

        # ALWAYS SWAP
        if turn == 2:
            return Move(-1, -1)

        move = select_best_move(board, self.colour)
        self._choices.remove(move)
        return move
