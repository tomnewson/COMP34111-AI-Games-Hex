from random import choice, shuffle
import math
from time import time

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

class Node:
    children: None # set in expansion
    parent: None # never changes

    state: Board # never changes
    prev_action: None | Move # never changes
    available_actions: list[Move] # never changes

    visits: int # increases in backpropagation
    value: float # increases in backpropagation
    our_turn: bool # never changes

    def __init__(self, state: Board, available_actions: list[Move], our_turn: bool, parent = None, prev_action = None):
        self.parent = parent
        self.state = state
        self.available_actions = available_actions
        self.visits = 0
        self.value = 0
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
    _time_limit: float = 5 # seconds per move
    _iterations: int = 1000
    EXPLORATION_CONSTANT = 2
    _parent_node_visits: int

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
            new_state: Board = self.copy_board(node.state)
            colour = self.colour if node.our_turn else self.opp_colour()
            new_state.set_tile_colour(action.x, action.y, colour)
            new_available_actions = [a for a in node.available_actions if a != action]
            node.children.append(Node(
                state=new_state,
                available_actions=new_available_actions,
                our_turn=not node.our_turn,
                parent=node,
                prev_action=action,
            ))

    def copy_board(self, board: Board):
        new_board = Board(board_size=self._board_size)
        for i in range(self._board_size):
            for j in range(self._board_size):
                new_board.set_tile_colour(i, j, board.tiles[i][j].colour)
        return new_board

    def simulation(self, node: Node):
        # play until no available actions remain
        available_actions = node.available_actions.copy()
        state = self.copy_board(node.state)
        our_turn = not node.our_turn
        shuffle(available_actions)
        while available_actions:
            action = available_actions.pop()
            state.set_tile_colour(action.x, action.y, self.colour if our_turn else self.opp_colour())
            our_turn = not our_turn
        return state.has_ended(self.colour)

    def backpropagation(self, node: Node, win: bool):
        while node:
            node.visits += 1
            if win and not node.our_turn:
                node.value += 1
            elif not win and node.our_turn:
                node.value += 1
            node = node.parent
        self._parent_node_visits += 1

    def mcts(self, board, available_actions):
        setup_mcts_start_time = time()
        root = Node(
            state=board,
            available_actions=available_actions,
            our_turn=True
        )
        self._parent_node_visits = 0
        # add first layer of children
        for action in available_actions:
            new_state: Board = self.copy_board(board)
            new_state.set_tile_colour(action.x, action.y, self.colour)
            new_available_actions = [a for a in available_actions if a != action]
            root.children.append(Node(
                state=new_state,
                available_actions=new_available_actions,
                our_turn=False,
                parent=root,
                prev_action=action,
            ))

        setup_mcts_time = time() - setup_mcts_start_time
        print(f"Setup MCTS time: {setup_mcts_time}")
        iterations = 0
        selection_times = []
        expansion_times = []
        simulation_times = []
        backpropagation_times = []
        while iterations < self._iterations:
            iterations += 1
            # Selection
            selection_start_time = time()
            leaf = self.selection(root)
            selection_times.append(time() - selection_start_time)
            # Expansion
            expansion_start_time = time()
            if leaf.visits > 0:
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

        move = self.mcts(board, self._choices)
        self._choices.remove(move)
        return move
