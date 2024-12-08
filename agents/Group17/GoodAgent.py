from random import choice, shuffle
from time import time
import math

from agents.Group17.chain import ChainFinder
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
    value: int = 0 # increases in backpropagation
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
    _max_iterations: int = 20_000
    EXPLORATION_CONSTANT = 2
    _parent_node_visits: int
    is_winning_chain = False
    virtual_connections = None

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

        return ChainFinder(state, self.colour).search(False)[0]

    def backpropagation(self, node: Node, win: bool):
        while node:
            node.visits += 1
            if win and not node.our_turn:
                node.value += 1
            elif not win and node.our_turn:
                node.value += 1
            node = node.parent
        self._parent_node_visits += 1

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
        print(f"Total setup time: {time() - start_time:.5f}s")

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

    def end_turn(self, move: Move):
        """remove from choices and return move"""
        if move not in self._choices:
            print(f"SOMETHING WENT WRONG, INVALID MOVE: {move}")
            print("MAKING RANDOM MOVE TO AVOID CRASH")
            move = choice(self._choices)

        print("MAKING MOVE: ", move)
        self._choices.remove(move)
        return move

    def get_neighbours(self, pos: tuple[int, int]) -> tuple[int,int]:
        """
        Returns a list of valid neighbouring nodes for a given node.
        """
        neighbour_offsets = [
            (-1, 0), (-1, 1),(0, 1),(1, 0), (1, -1),(0, -1),

        ]

        neighbours = []

        for dx, dy in neighbour_offsets:
            nx, ny = pos[0] + dx, pos[1] + dy
            if  0 <= nx < self._board_size and 0 <= ny < self._board_size:
                neighbours.append((nx,ny))

        return neighbours

    def find_winning_move_from(self, state: list[list[Colour | None]], tile: tuple[int,int], visited: list) -> Move | None:
        for neighbour in self.get_neighbours(tile):
            nx, ny = neighbour
            if state[nx][ny] is None and neighbour not in visited:
                visited.append(neighbour)
                new_state = self.copy_state(state)
                new_state[nx][ny] = self.colour
                if ChainFinder(new_state, self.colour).search(False)[0]:
                    print(f"immediate win: {neighbour}")
                    return Move(nx, ny)
        return None

    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        start_time = time()

        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove(opp_move)

        # ALWAYS SWAP
        if turn == 2:
            return Move(-1, -1)

        state = [[tile.colour for tile in row] for row in board.tiles]

        # manual check for immediate win
        immediate_win_check_start_time = time()
        visited = []
        for x in range(self._board_size):
            for y in range(self._board_size):
                if state[x][y] == self.colour:
                    winning_move = self.find_winning_move_from(state, (x, y), visited)
                    if winning_move:
                        return self.end_turn(winning_move)
        print(f"Immediate win check time: {time() - immediate_win_check_start_time:.5f}s")

        winning_chain_check_start_time = time()
        # check for winning chains
        if not self.is_winning_chain:
            self.is_winning_chain, self.virtual_connections = ChainFinder(state, self.colour).search()
        if self.is_winning_chain:
            print(f"virtual connections in winning chain: {self.virtual_connections}")
            for pair in self.virtual_connections:
                x1, y1 = pair[0]
                x2, y2 = pair[1]
                if state[x1][y1] == self.opp_colour() and state[x2][y2] is None:
                    self.virtual_connections.remove(pair)
                    return self.end_turn(Move(x2, y2))
                if state[x2][y2] == self.opp_colour() and state[x1][y1] is None:
                    self.virtual_connections.remove(pair)
                    return self.end_turn(Move(x1, y1))
            if self.virtual_connections:
                for pair in self.virtual_connections:
                    x1, y1 = pair[0]
                    x2, y2 = pair[1]
                    if state[x1][y1] is None:
                        self.virtual_connections.remove(pair)
                        return self.end_turn(Move(x1, y1))
                    if state[x2][y2] is None:
                        self.virtual_connections.remove(pair)
                        return self.end_turn(Move(x2, y2))
        print(f"Winning chain check time: {time() - winning_chain_check_start_time:.5f}s")

        move = self.mcts(state, self._choices, start_time)
        return self.end_turn(move)
