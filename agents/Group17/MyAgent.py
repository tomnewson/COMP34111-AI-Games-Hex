from random import choice
import time
import math
import copy

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

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
    _time_limit: float = 10 # seconds per move
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

        def __init__(self, board: Board, actions: list[Move], parent = None, action = None):
            self.board = board
            self.actions = actions
            self.parent = parent
            self.action = action
            self.children = []
            self.total_score = 0
            self.visits = 0

        def add_child(self, child):
            """Expand node"""
            self.children.append(child)

        def root_visits(self):
            """Return the number of visits of the root node"""
            if self.parent is None:
                return self.visits
            return self.parent.root_visits()

        # Call UCT for each child node in a function to evaluate
        # which one is higher
        def UCT(self, risk):
            """Upper Confidence Bound for Trees"""
            if self.visits == 0:
                return math.inf

            average_value = self.total_score / self.visits
            exploration = risk * (math.sqrt(math.log(self.root_visits()) / self.visits))

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

        def expand(self):
            """MCTS Expansion phase
            what are the node's actions?
            for each action, create a new node with the resulting state
            add the new node as a child of the current node
            """
            print("?>@:~:?>@:?>:@?>:@?>:@")
            for move in self.actions:
                new_actions = copy.deepcopy(self.actions)
                new_actions.remove(move)
                new_board = copy.deepcopy(self.board)
                new_board.set_tile_colour(move.x, move.y, MyAgent.colour)

                self.add_child(
                    MyAgent.Node(
                        board=new_board,
                        parent=self,
                        actions=new_actions,
                        action = move,
                    )
                )
                # print(self.children, "£$&*()&^%$^&*")

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
        attempts = 3
        total_res = 0
        for _ in range(attempts):
            final_board = self.play(node.board, node.actions, False)
            total_res += self.get_result(final_board)
        self.backpropagate(node, total_res / attempts)
        print("##################", total_res)

    def play(self, board: Board, available_actions: list[Move], our_turn: bool):
        """Play until no actions
        Return board"""
        if not available_actions:
            return board

        new_actions = copy.deepcopy(available_actions)
        colour = self.colour if our_turn else self.opp_colour()
        move = choice(new_actions)
        new_actions.remove(move)

        new_board = copy.deepcopy(board)
        new_board.set_tile_colour(move.x, move.y, colour)

        return self.play(new_board, new_actions, not our_turn)


    def backpropagate(self, node: Node, result: float):
        """MCTS Backpropagation phase"""
        node.visits += 1
        node.total_score += result

        if node.parent:
            self.backpropagate(node.parent, result)

    def mcts(self, board: Board, start_time: float):
        """Monte Carlo Tree Search
        Each node in tree is a Board"""
        root = MyAgent.Node(copy.deepcopy(board), actions=copy.deepcopy(self._choices))

        while True:
            time_elapsed = time.time() - start_time
            if time_elapsed >= self._time_limit:
                break

            # Selection
            leaf = self.select_node(root)

            print(leaf.visits)
            if leaf.visits > 0 and leaf.actions:
                # Expansion
                leaf.expand()
                # print(leaf.children, ")((*((*&(*&*&(*&(&**&)))))))")
                leaf = leaf.children[0]
            # Play/Rollout
            # do we want to playout from terminal nodes?
            self.playout(leaf)
            print("~~~~~~~~~~~~~~~~~~~~~")

        # print(leaf.children, root.children, "!!!!!!!!!!")
        if root.children:
            for child in root.children:
                print(child.total_score)
            move = root.best_child(0).action
            print(f"move: {move}, value: {root.best_child(0).total_score }")
            return move
        print("failed, picking randomly")
        return -1

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

        # Swap with 50% chance
        if turn == 2 and choice([0, 1]) == 1:
            return Move(-1, -1)

        move = self.mcts(board, time.time())
        print(move)
        self._choices.remove(move)
        return move
