from random import choice
import time
import math
import copy

from src.AgentBase import AgentBase
from src.Board import Board
from src.Colour import Colour
from src.Move import Move
from haswin import has_winning_chain


def winvalue(B: Board, player: Colour):
    print("**********************")
    print(11)
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
