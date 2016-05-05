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
    points = [255] * board.length

    for coord in range(board.length):
        color = board.at(coord)

        if color == EMPTY or board.is_marked_dead(coord):
            continue

        for n in neighbors(coord, board.size):
            _flood_assign(board, points, n, color)

    return points


def _flood_assign(board, points, origin, color):
    def flood(coord):
        if not board.is_marked_dead(coord) and board.at(coord) == opposite(color):
            return False

        if points[coord] == color:
            return True

        points[coord] = color

        if board.at(coord) == color:
            return True

        for n in neighbors(coord, board.size):
            if not flood(n):
                return False

        return True

    return flood(origin)


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
