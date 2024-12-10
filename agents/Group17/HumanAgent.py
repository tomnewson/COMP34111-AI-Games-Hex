from agents.Group17.GoodAgent import GoodAgent
from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move

class HumanAgent(AgentBase):
    _choices: list[Move]
    _board_size: int = 11

    def __init__(self, colour: Colour):
        super().__init__(colour)
        self._choices = [
            Move(i, j) for i in range(self._board_size) for j in range(self._board_size)
        ]

    def make_move(self, turn: int, board: Board, opp_move: Move | None) -> Move:
        if opp_move and opp_move != Move(-1, -1):
            self._choices.remove(opp_move)

        print("""Enter your move in the format 'x y'
            e.g. bottom left: 10 0
            or enter 'help' to ask the agent for the best move.""".replace("    ", ""))
        if turn == 2:
            print("or enter 'swap' to swap")

        while True:
            inp = input("Your move: ").strip().lower()
            if inp == "help":
                move = GoodAgent(self.colour).make_move(turn, board, opp_move)
                print("Starting Board:\n" + board.print_board())
                if move == Move(-1, -1):
                    print("Agent suggests: swap")
                else:
                    print(f"Agent suggests: {move.x} {move.y}")
                continue
            if inp == "swap" and turn == 2:
                return Move(-1, -1)
            try:
                x, y = map(int, inp.split())
                move = Move(x, y)
                if not (0 <= x < self._board_size and 0 <= y < self._board_size):
                    print("Invalid move: out of bounds")
                    continue
                if move not in self._choices:
                    print("Invalid move: tile already occupied")
                    continue
                self._choices.remove(move)
                return move
            except ValueError:
                print("Invalid move: please enter two integers separated by a space")
