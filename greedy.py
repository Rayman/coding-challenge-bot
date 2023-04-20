"""
A coding challenge bot that tries to determine the best move by looking at the squares next to it\
"""

from random import choice

import numpy as np

from ..bot_control import Move


def determine_new_tile_colour(floor_colour, bot_colour):
    if floor_colour == 0: return bot_colour  # Bot always paints a white floor tile
    return [floor_colour, 0, bot_colour][(bot_colour - floor_colour) % 3]


class Greedy:

    def __init__(self):
        self.target = None

    def get_name(self):
        return "Greedy Gerard"

    def get_contributor(self):
        return "Rayman"

    def determine_next_move(self, grid, enemies, game_info):
        moves = {
            Move.UP: np.array([0, 1], dtype=np.int16),
            Move.RIGHT: np.array([1, 0], dtype=np.int16),
            Move.LEFT: np.array([-1, 0], dtype=np.int16),
            Move.DOWN: np.array([0, -1], dtype=np.int16),
        }

        moves_with_points = []
        for value, move in moves.items():
            target = self.position + move
            try:
                color = grid[target[1], target[0]]
            except IndexError:
                continue
            is_points = color != self.id and determine_new_tile_colour(color, self.id) == self.id
            if is_points:
                moves_with_points.append(value)

        if moves_with_points:
            return choice(moves_with_points)
        else:
            return choice(list(moves.keys()))
