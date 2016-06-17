# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import namedtuple

from weiqi.board import EMPTY, BLACK, WHITE, neighbors, opposite

Score = namedtuple('Score', ['white', 'black', 'komi', 'handicap', 'winner', 'win_by', 'result', 'points'])


def count_score(board, komi) -> Score:
    points = _assign_points(board)
    return _count_points(points, komi, board.handicap)


def _assign_points(board):
    points = [EMPTY] * board.length

    for coord in range(board.length):
        if points[coord] != EMPTY:
            continue

        only_black, visited = can_reach_only(board, coord, BLACK)
        if only_black:
            for c in visited:
                points[c] = BLACK
            continue

        only_white, visited = can_reach_only(board, coord, WHITE)
        if only_white:
            for c in visited:
                points[c] = WHITE
            continue

    return points


def can_reach_only(board, coord, color, visited=None):
    """Checks if from a given origin only stones of the given color can be reached."""
    if not visited:
        visited = set()
    elif coord in visited:
        return True, visited

    visited.add(coord)

    if not board.is_marked_dead(coord) and board.at(coord) == color:
        return True, visited

    if not board.is_marked_dead(coord) and board.at(coord) == opposite(color):
        return False, visited

    for n in neighbors(coord, board.size):
        if not can_reach_only(board, n, color, visited)[0]:
            return False, visited

    return True, visited


def _count_points(points, komi, handicap):
    white = points.count(WHITE)
    black = points.count(BLACK)

    white += komi
    white += handicap

    winner = WHITE if white > black else BLACK
    win_by = abs(white-black)

    if winner == WHITE:
        result = "W+{:.1f}".format(win_by)
    else:
        result = "B+{:.1f}".format(win_by)

    return Score(white, black, komi, handicap, winner, win_by, result, points)
