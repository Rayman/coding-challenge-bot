from abc import ABC, abstractmethod
from collections import deque
from heapq import heappush, heappop
from random import choice

import numpy as np

from ..bot_control import Move

__all__ = ['Abra', 'Kadabra', 'Alakazam']


def find_best_moves(grid, position, max_depth, id, previous_positions=None):
    """
    :return: Tuple of move, score pairs
    """
    # print(f'find_best_moves')

    if previous_positions is None:
        previous_positions = []

    score_grid = calculate_score_grid(grid, id)

    # penalize deadlock positions
    for deadlock_position, count in calculate_deadlock_positions(position, previous_positions):
        # print(f'possible deadlock position={deadlock_position} count={count} current_position={position} previous_positions={np.array(previous_positions).tolist()}')
        # sleep(0.5)
        score_grid[deadlock_position[1], deadlock_position[0]] -= count

    open_set = PriorityQueue()
    open_set.push(Node(depth=max_depth + 1, current_score=0., history=np.array([position]), score_grid=score_grid))

    best_score = float('-inf')
    best_nodes = []
    while open_set:
        node = open_set.pop()
        # print(f'exploring: {node}')

        if node.depth == 0:  # node finished exploring
            if node.upper_bound > best_score:
                best_score = node.upper_bound
                best_nodes = [node]
            elif node.current_score == best_score:
                best_nodes.append(node)

        if node.upper_bound < best_score:
            # all nodes that come after this node will have an even lower upper_bound. There will never be any node
            # that can increase best_score, so we can quit
            break

        for neighbor in node.neighbors():
            if neighbor.upper_bound < best_score:
                # don't even bother pushing this node, it will never be higher than best_score
                # print(f'skipping node={neighbor}')
                continue
            open_set.push(neighbor)

    # global mat
    # data = np.copy(score_grid)
    # data = np.power(data, 3)
    # # for node in best_nodes:
    # #     for p in node.history:
    # #         data[p[1], p[0]] = -0.1
    # data[position[1], position[0]] = -0.2
    # if not mat:
    #     mat = plt.matshow(data, vmin=-0.2, vmax=1, origin='lower', cmap=matplotlib.cm.rainbow)
    # else:
    #     mat.set_data(data)
    # plt.draw()
    # plt.pause(1e-6)

    # print(f'best_nodes={best_nodes}')
    for node in best_nodes:
        yield node.history[1] - node.history[0], node.current_score


class Node:
    __slots__ = ('depth', 'current_score', 'history', 'score_grid', 'upper_bound')

    def __init__(self, depth, current_score, history, score_grid):
        assert isinstance(depth, int), type(depth)
        assert isinstance(current_score, float), type(current_score)
        assert isinstance(history, np.ndarray), type(history)
        assert isinstance(score_grid, np.ndarray), type(score_grid)
        self.depth = depth
        self.current_score = current_score
        self.history = history
        self.score_grid = score_grid
        self.upper_bound = current_score + depth

    def neighbors(self):
        if self.depth > 0:
            last_move = self.history[-1]
            if last_move[0] > 0:
                yield from self.possible_neighbor(last_move + LEFT)
            if last_move[1] > 0:
                yield from self.possible_neighbor(last_move + DOWN)
            if last_move[0] < self.score_grid.shape[1] - 1:
                yield from self.possible_neighbor(last_move + RIGHT)
            if last_move[1] < self.score_grid.shape[0] - 1:
                yield from self.possible_neighbor(last_move + UP)

    def possible_neighbor(self, next_position):
        if (self.history[1:] == next_position).all(axis=1).any():
            return
        next_score = self.current_score + self.score_grid[next_position[1], next_position[0]]
        yield Node(self.depth - 1, next_score, np.concatenate((self.history, next_position[np.newaxis, ...])),
                   self.score_grid)

    def __lt__(self, other):
        """The highest priority node (lowest) is the one with the highest possible score"""
        # return self.current_score < other.current_score
        return self.upper_bound > other.upper_bound

    def __repr__(self):
        return f"{self.__class__.__name__}(depth={self.depth} current_score={self.current_score:.2f} history={self.history.tolist()})"


def calculate_score_grid(grid: np.array, id):
    scores = dict(zip(*np.unique(grid, return_counts=True)))
    scores.pop(0, None)

    weights = np.zeros_like(grid, dtype=float)
    grid_modulo = (id - grid) % 3
    weights[(grid == 0)] = 1  # white
    weights[(grid != id) & (grid_modulo == 2)] = 1  # taking
    # weights[(grid != id) & (grid != 0) & (grid_modulo != 0)] += 1e-6  # converting an enemy

    scaling = 10
    max_score = max(scores.values()) if scores else 1
    for color, score in scores.items():
        if color == id or (id - color) % 3 == 0:
            continue
        # bonus for converting other players
        weights[grid == color] += score / max_score / scaling
    weights /= 1 + 1 / scaling
    assert (weights <= 1).all(), weights
    assert (weights >= 0).all(), weights
    return weights


def calculate_deadlock_positions(position, previous_positions):
    """
    :return: Which positions to avoid
    """
    if not previous_positions:
        return
    unique_positions, counts = np.unique(np.vstack((position, previous_positions)), axis=0, return_counts=True)
    for i, count in enumerate(counts):
        if count > 1:
            yield unique_positions[i], count


class PriorityQueue:
    __slots__ = ('heap',)

    def __init__(self):
        self.heap = []

    def push(self, item):
        heappush(self.heap, item)

    def pop(self):
        return heappop(self.heap)

    def __bool__(self):
        return bool(self.heap)


UP = np.array([0, 1], dtype=np.int16)
RIGHT = np.array([1, 0], dtype=np.int16)
LEFT = np.array([-1, 0], dtype=np.int16)
DOWN = np.array([0, -1], dtype=np.int16)

moves = {
    Move.UP: UP,
    Move.RIGHT: RIGHT,
    Move.LEFT: LEFT,
    Move.DOWN: DOWN,
}


def direction_to_move(direction):
    """Return Move enum value from a numpy direction"""
    return next(value for value, move in moves.items() if np.array_equal(move, direction))


mat = None


##############
# Public API #
##############

class Bot(ABC):
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.id = None  # will be set by the game
        self.position = None  # will be set by the game
        self.previous_positions = deque([], maxlen=8)

    @abstractmethod
    def get_name(self):
        raise NotImplementedError()

    def get_contributor(self):
        return "Rayman"

    def determine_next_move(self, grid, enemies, game_info):
        # print('\ndetermine_next_move\n')
        direction, _ = choice(
            list(find_best_moves(grid, self.position, self.max_depth, self.id, self.previous_positions)))
        self.previous_positions.appendleft(self.position)  # update after find_best_moves
        move = direction_to_move(direction)
        return move


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
        super().__init__(5)

    def get_name(self):
        return 'Alakazam'
