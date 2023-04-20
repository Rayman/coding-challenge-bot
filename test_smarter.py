import os.path
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from robots.rayman.smarter import Move, score_all_moves, direction_to_move, calculate_score_grid


def test_calculate_score_grid():
    grid = np.array([[0, 1, 2, 3, 4]])
    scores = calculate_score_grid(grid, 4)

    assert scores[0, 0] == 1, 'white'
    assert scores[0, 1] == 0, "enemy that can't be taken"
    assert scores[0, 2] == 1 + 1e-6, 'enemy that can be overwritten'
    assert scores[0, 3] == 1e-6, 'enemy that converts to white'
    assert scores[0, 4] == 0, 'own tile stays the same'


def test_out_of_bounds():
    grid = np.array([[4]])
    position = (0, 0)
    scores = [s for m, s in score_all_moves(grid, position, 0, 4)]
    assert all(score == float('-inf') for score in scores)


def test_out_of_bounds2():
    grid = np.array([[4, 4]])
    position = (0, 0)
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.LEFT] == float('-inf')
    assert moves_with_scores[Move.RIGHT] == 0
    assert moves_with_scores[Move.UP] == float('-inf')
    assert moves_with_scores[Move.DOWN] == float('-inf')


def test_avoid_own_color():
    grid = np.array([[4, 4],
                     [0, 0]])
    position = (0, 0)
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.RIGHT] == 0
    assert moves_with_scores[Move.UP] > moves_with_scores[Move.RIGHT]


def test_avoid_enemies_that_cant_be_taken():
    grid = np.array([[4, 1],
                     [0, 0]])
    position = (0, 0)
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.UP] > 0 == moves_with_scores[Move.RIGHT]


def test_prefer_to_take_enemies():
    grid = np.array([[4, 2],
                     [0, 0]])
    position = (0, 0)
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.RIGHT] > moves_with_scores[Move.UP] > 0


def test_prefer_to_convert_to_white():
    grid = np.array([[4, 3],
                     [4, 0]])
    position = (0, 0)
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.RIGHT] > 0 == moves_with_scores[Move.UP]


def test_should_not_get_stuck():
    grid = np.array([[4, 0, 4],
                     [0, 4, 4],
                     [0, 4, 4]])
    position = np.array([0, 0])

    # with a depth of 0, both directions should be equal
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 0, 4)}
    assert moves_with_scores[Move.UP] == moves_with_scores[Move.RIGHT] > 0

    # with a depth of 1, the dead end should be seen
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 1, 4)}
    assert moves_with_scores[Move.UP] > moves_with_scores[Move.RIGHT] > 0


def test_should_not_evaluate_going_back():
    grid = np.array([[4, 0, 0],
                     [0, 4, 4],
                     [0, 0, 4]])
    position = np.array([0, 0])
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 2, 4)}
    assert moves_with_scores[Move.UP] > moves_with_scores[Move.RIGHT] > 0


def test_can_evaluate_starting_position():
    """
    Going back over previous moves doesn't work because the algorithm doesn't keep track of grid scores. But going back
    over the starting position might be advantagious becuase it could be converted to white
    """
    grid = np.array([[0, 0, 0],
                     [0, 4, 4]])
    position = np.array([0, 0])
    moves_with_scores = {direction_to_move(m): s for m, s in score_all_moves(grid, position, 3, 4)}
    assert moves_with_scores[Move.UP] > moves_with_scores[Move.RIGHT] > 0
