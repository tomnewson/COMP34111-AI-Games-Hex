from random import choice

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

class Node:
    """Node class for MCTS"""
    board: Board
    parent: Node | None
    children: list[Node]

    def __init__(self, board: Board, parent: Node|None = None):
        self.board = board
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)


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
    _time_limit: int = 5 # seconds per move

    def __init__(self, colour: Colour):
        super().__init__(colour)
        self._choices = [
            (i, j) for i in range(self._board_size) for j in range(self._board_size)
        ]

    def select_node(self, node: Node):
        """MCTS Selection phase
        Call best_child() with exploration constant reflecting the balance between exploration and exploitation
        Return selection
        """
        pass

    def is_terminal(self, node: Node):
        """Return True if the node is a win/loss, False otherwise"""
        pass

    def get_result(self, node: Node):
        """Return 1 for win, -1 for loss"""
        pass

    def expand_node(self, node: Node):
        """MCTS Expansion phase
        Make untried move from node
        Add to tree as a child
        Return child
        """
        pass

    def playout(self, node: Node):
        """MCTS Playout phase
        Apply policy until move is terminal
        Return result
        """
        pass

    def backpropagate(self, node: Node, result: int):
        """MCTS Backpropagation phase"""
        pass

    def best_child(self, node: Node, exploration_constant: float):
        """Return child with best UCT value"""
        pass

    def mcts(self, board: Board, choices: list[Move], time_limit: int, start_time: float):
        """Monte Carlo Tree Search
        Each node in tree is a Board"""

        root = Node(board)

        time_elapsed = time.time() - start_time

        while True:
            if time_elapsed >= self._time_limit:
                break

            # Selection
            leaf = select_node(root)
            if is_terminal(leaf):
                result = get_result(leaf)
            else:
                # Expansion
                child = expand_node(leaf)
                # Playout
                result = playout(child)
            # Backpropagation
            backpropagate(child, result)

        # Return best child when time's up (maximise exploitation)
        return best_child(root, exploration_constant=0)

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

        start_time = time.time()

        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove((opp_move.x, opp_move.y))

        # Swap with 50% chance
        if turn == 2 and choice([0, 1]) == 1:
            return Move(-1, -1)

        # move = self.mcts()

        x, y = choice(self._choices)
        move = Move(x, y)

        self._choices.remove((move.x, move.y))
        return move
