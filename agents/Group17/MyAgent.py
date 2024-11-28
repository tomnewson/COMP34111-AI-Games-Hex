from random import choice
import time
import math

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

class Node:
    """Node class for MCTS"""
    board: Board
    parent: None
    children: None
    total_score: int
    visits: int

    def __init__(self, board: Board, parent = None, total_score = 0, visits = 0):
        self.board = board
        self.parent = parent
        self.children = []
        self.total_score = total_score
        self.visits = visits

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
        # shit way to get the visits of the root node (N)
        p = self
        while True:
            if p.parent is None:
                root_visits = self.visits
                break
            p = p.parent

        exploration = risk * (math.sqrt(math.log(root_visits) / self.visits))

        return average_value + exploration

    def best_child(self, risk = 2):
        best_child = (None, -math.inf)

        for child in self.children:
            if child.visits == 0:
                return child
            uct = child.UCT(risk)
            if uct > best_child[1]:
                best_child = (child, uct)
        return best_child[0]

    def is_terminal(self):
        """Return True if the node is a win/loss, False otherwise"""
        return self.board.has_ended(Colour.RED) or self.board.has_ended(Colour.BLUE)


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
    _time_limit: int = 1 # seconds per move
    EXPLORATION_CONSTANT = 2

    def __init__(self, colour: Colour):
        super().__init__(colour)
        self._choices = [
            (i, j) for i in range(self._board_size) for j in range(self._board_size)
        ]

    def select_node(self, node: Node):
        """MCTS Selection phase
        Call best_child() with exploration constant reflecting the balance between exploration and exploitation
        Repeat until leaf node is reached
        Return selection
        """
        while True:
            if not node.children:
                return node # return leaf node
            node = node.best_child(self.EXPLORATION_CONSTANT)

    def get_result(self, node: Node):
        """Return 1 for win, -1 for loss"""
        return 1

    def expand_node(self, node: Node):
        """MCTS Expansion phase
        Make untried move from node
        Add to tree as a child
        Return child
        """
        return node

    def playout(self, node: Node):
        """MCTS Playout phase
        Apply policy until move is terminal
        Backpropagate result
        Return result
        """
        # Backpropagation
        child = node # Placeholder
        result = 1
        self.backpropagate(child, result)
        return self.get_result(node)

    def backpropagate(self, node: Node, result: int):
        """MCTS Backpropagation phase"""

    def mcts(self, board: Board, start_time: float):
        """Monte Carlo Tree Search
        Each node in tree is a Board"""

        root = Node(board)

        while True:
            time_elapsed = time.time() - start_time
            if time_elapsed >= self._time_limit:
                break

            # Selection
            leaf = self.select_node(root)

            if leaf.visits > 0:
                # Expansion
                self.expand_node(leaf)
                leaf = leaf.children[0]
            # Play/Rollout
            self.playout(leaf)

        # Return best child when time's up (maximise exploitation)
        # return root.best_child(self.EXPLORATION_CONSTANT)
        return self._pick_random_move(self._choices) # placeholder return until mcts is implemented

    def _pick_random_move(self, choices):
        """Pick a random move from the list of choices"""
        x, y = choice(choices)
        return Move(x, y)

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
            self._choices.remove((opp_move.x, opp_move.y))

        # Swap with 50% chance
        if turn == 2 and choice([0, 1]) == 1:
            return Move(-1, -1)

        move = self.mcts(board, time.time())

        self._choices.remove((move.x, move.y))
        return move
