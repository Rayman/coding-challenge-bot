from random import randrange, choice

import numpy as np

from ..bot_control import Move


class Follower:
    def __init__(self):
        self.id = None  # will be set by the game
        self.position = None  # will be set by the game
        self.target_id = None

    def get_name(self):
        return 'Follower'

    def get_contributor(self):
        return 'Rayman'

    def determine_next_move(self, grid, enemies, game_info):
        if randrange((grid.shape[0] + grid.shape[1]) * 4) == 0 or game_info.current_round == 1:
            scores = dict(zip(*np.unique(grid, return_counts=True)))
            scores.pop(0, None)
            scores.pop(self.id, None)
            scores = {color: score for color, score in scores.items() if (self.id - color) % 3 == 2}
            if not scores:
                return Move.STAY

            self.target_id = choice([s for s in scores])
            # self.target_id = max(scores, key=lambda color: scores[color])

        target = next((enemy for enemy in enemies if enemy['id'] == self.target_id), None)
        if target is None:
            return Move.STAY
        target_pos = target['position']
        return self.move_to_position(target_pos)

    def move_to_position(self, position):
        dx, dy = position - self.position
        if abs(dx) > abs(dy):
            if dx > 0:
                return Move.RIGHT
            else:
                return Move.LEFT
        else:
            if dy > 0:
                return Move.UP
            else:
                return Move.DOWN
