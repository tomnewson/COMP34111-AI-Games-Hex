from random import choice
import time
import math
import copy

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move
from agents.Group17.haswin import has_winning_chain


def winvalue(B: Board, player: Colour):
    """
    Computes the winvalue of a given board configuration B for player.

    Args:
        B: The board configuration (a data structure representing the game state).
        player: The current player to move.

    Returns:
        tuple: (v, X) where v is 1/-1 if the player wins/loses and X is a win-set.
    """
    tiles = [[tile.colour for tile in row] for row in B.tiles]
    # Check if the current player has a winning chain
    if has_winning_chain(tiles, player):
        # print(player)
        # print(B.print_board())
        # raise Exception("Player has a winning chain")
        # print("PLAYER WIN")
        return (+1, set())

    opponent = get_opponent(player)
    # Check if the opponent has a winning chain
    if has_winning_chain(tiles, opponent):
        # print("OPPONENT WIN")
        return (-1, set())

    # Initialize W (the win-set) and M (the must-play cells)
    W = set()
    M = get_unoccupied_cells(B)

    # Iterate while there are still cells to consider
    loop = 0
    while M:
        loop += 1
        # print("loop" + str(loop))
        cell = M.pop()

        B_next = copy.deepcopy(B)
        # Simulate the board after placing the player's stone in cell m
        B_next = sim_move(B, cell, player)

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

    for row in range(0,11):
        for col in range(0,11):
            if B.tiles[row][col].colour is None:  # Check if the tile is unoccupied
                unoccupied_cells.add((row, col))

    return unoccupied_cells

def sim_move(SIM_B: Board, cell: tuple[int, int], player: Colour):
    x, y = cell
    SIM_B.tiles[x][y].colour = player
    return SIM_B

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
        sim_move(simulated_board, cell, player)

        # Evaluate the board state after the simulated move
        value, win_set = winvalue(simulated_board, get_opponent(player))

        # If this move guarantees a loss
        if value == -1:
            return Move(cell[0], cell[1])


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
