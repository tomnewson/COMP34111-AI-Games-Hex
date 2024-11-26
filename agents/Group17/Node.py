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
