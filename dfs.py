"""
A coding challenge bot that searches for the best move by going trough all combination of moves
"""

from abc import ABC, abstractmethod
from random import choice

import numpy as np

from ..bot_control import Move

__all__ = ['Abra', 'Kadabra']


def score_move(score_grid, history, current_score, depth, id):
    last_move = history[-1]
    # check for out of bounds
    if last_move[0] < 0 or last_move[1] < 0 or \
            last_move[0] >= score_grid.shape[1] or last_move[1] >= score_grid.shape[0]:
        return float('-inf')

    current_score += score_grid[history[-1][1], history[-1][0]]
    # print(f'score_move: depth={depth} current_score={current_score} history={history}')
    if depth == 0:
        score = current_score
    else:
        max_score = float('-inf')
        for move in moves.values():
            next_position = last_move + move
            if [h for h in reversed(history[1:]) if np.array_equal(next_position, h)]:
                continue
            max_score = max(max_score, score_move(score_grid, history + [next_position], current_score, depth - 1, id))
        score = max_score

    # print(f'calculate_best_move: score={score}\tdepth={depth} history={history}')
    return score


def score_all_moves(grid, position, max_depth, id):
    """
    :return: Tuple of move, score pairs
    """
    # print('score_all_moves')
    score_grid = calculate_score_grid(grid, id)
    return [(move, score_move(score_grid, [position, position + move], 0, max_depth, id)) for move in moves.values()]


def calculate_score_grid(grid: np.array, id):
    score = np.zeros_like(grid, dtype=float)
    grid_modulo = (id - grid) % 3
    score[(grid == 0)] = 1  # white
    score[(grid != id) & (grid_modulo == 2)] = 1  # taking
    score[(grid != id) & (grid != 0) & (grid_modulo != 0)] += 1e-6  # converting enemy
    return score


moves = {
    Move.UP: np.array([0, 1], dtype=np.int16),
    Move.RIGHT: np.array([1, 0], dtype=np.int16),
    Move.LEFT: np.array([-1, 0], dtype=np.int16),
    Move.DOWN: np.array([0, -1], dtype=np.int16),
}

sentinel = object()


def random_max(it, *, key):
    it = iter(it)
    largest = next(it, sentinel)
    if largest is sentinel:
        raise ValueError('max() arg is an empty sequence')
    largest_value = key(largest)
    largests = [largest]
    for x in it:
        value = key(x)
        if value > largest_value:
            largests = [x]
            largest_value = value
        elif value == largest_value:
            largests.append(x)
    return choice(largests)


def direction_to_move(direction):
    """Return Move enum value from a numpy direction"""
    return next(value for value, move in moves.items() if np.array_equal(move, direction))


##############
# Public API #
##############

class Bot(ABC):
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.id = None  # will be set by the game
        self.position = None  # will be set by the game

    @abstractmethod
    def get_name(self):
        raise NotImplementedError()

    def get_contributor(self):
        return "Rayman"

    def determine_next_move(self, grid, enemies, game_info):
        # print('\ndetermine_next_move\n')
        next_move, _ = random_max(score_all_moves(grid, self.position, self.max_depth, self.id), key=lambda m: m[1])
        return direction_to_move(next_move)


class Abra(Bot):
    def __init__(self):
        super().__init__(0)

    def get_name(self):
        return 'Abra'


class Kadabra(Bot):
    def __init__(self):
        super().__init__(1)

    def get_name(self):
        return 'Kadabra'


class Alakazam(Bot):
    def __init__(self):
        super().__init__(2)

    def get_name(self):
        return 'Alakazam'
