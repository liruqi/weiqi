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

import re

BLACK = 'x'
WHITE = 'o'
EMPTY = '.'

PASS = -1
RESIGN = -2

NODE_BLACK = 'B'
NODE_WHITE = 'W'
NODE_EDIT = 'E'

SYMBOL_TRIANGLE = 'TR'
SYMBOL_SQUARE = 'SQ'
SYMBOL_CIRCLE = 'CR'


def coord2d(x, y, size=9):
    return (y-1)*size + (x-1)


def coord_to_2d(coord, size):
    y = int(coord / size)
    x = coord - y*size
    return (x+1), (y+1)


def neighbors(coord, size):
    x, y = coord_to_2d(coord, size)
    x -= 1
    y -= 1
    n = []

    if y > 0:
        n.append(coord - size)
    if y < size-1:
        n.append(coord + size)
    if x > 0:
        n.append(coord - 1)
    if x < size-1:
        n.append(coord + 1)

    return n


def validate_move(move, size):
    if move < RESIGN or move >= size*size:
        raise ValueError('invalid move: {}'.format(move))


class Node:
    def __init__(self):
        self.id = None
        self.parent_id = None
        self.children = []

        self.action = None
        self.move = None  # Used for actions NODE_BLACK and NODE_WHITE
        self.edits = []  # Used for action NODE_EDIT

        self.captures = []  # Only set for actions NODE_BLACK and NODE_WHITE
        self.marked_dead = {}
        self.score_points = []
        self.labels = []
        self.symbols = []


class IllegalMoveError(Exception):
    pass


class Board:
    def __init__(self, size=9):
        self.size = size
        self.current = BLACK
        self.tree = []
        self.pos = [EMPTY]*size*size
        self.current_node_id = None

    def __str__(self):
        board = ''

        for i, c in enumerate(self.pos):
            board += c

            if (i+1) % self.size == 0:
                board += '\n'

        return board

    def at(self, coord):
        return self.pos[coord]

    @property
    def current_node(self) -> Node:
        return self.tree[self.current_node_id] if self.current_node_id is not None else None

    @property
    def ko(self) -> int:
        if not self.current_node:
            return None

        if len(self.current_node.captures) == 1:
            return self.current_node.captures[0]
        return None

    @property
    def both_passed(self):
        if len(self.tree) < 2:
            return False

        if self.current_node.parent_id is None or self.current_node.move != PASS:
            return False

        return self.tree[self.current_node.parent_id].move == PASS

    def play(self, move):
        validate_move(move, self.size)

        if move in [PASS, RESIGN]:
            self._add_move(move)
            self.current = WHITE if self.current == BLACK else BLACK
            return

        self.validate_legal(move)

        caps = self._find_captures(move)
        for c in caps:
            self.pos[c] = EMPTY

        self.pos[move] = self.current
        self._add_move(move, caps)
        self.current = WHITE if self.current == BLACK else BLACK

    def validate_legal(self, coord):
        if self.at(coord) != EMPTY:
            raise IllegalMoveError('coordinate is not empty')

        if coord == self.ko:
            raise IllegalMoveError('coordinate is a ko point')

        if self.is_suicide(coord):
            raise IllegalMoveError('coordinate is a suicide')

    def is_suicide(self, coord):
        """Checks if the given move is a suicide for the current player.
        A move is not suicide if any of the following conditions holds true:
        - any neighboring point is empty
        - any neighboring point is the same color and has more than one liberty
        - any neighboring point is a different color and has only one liberty
        """
        for n in neighbors(coord, self.size):
            color = self.at(n)

            if color == EMPTY:
                return False

            chain = self.chain_at(n)
            libs = len(self.chain_liberties(chain))

            if color == self.current and libs > 1:
                return False

            if color != self.current and libs == 1:
                return False

        return True

    def _find_captures(self, coord):
        caps = set()

        for n in neighbors(coord, self.size):
            if self.at(n) == EMPTY or self.at(n) == self.current:
                continue

            chain = self.chain_at(n)
            if len(self.chain_liberties(chain)) <= 1:
                caps |= chain

        return caps

    def chain_at(self, coord) -> set:
        chain = set()
        color = self.at(coord)

        if color == EMPTY:
            return chain

        def populate(c):
            for n in neighbors(c, self.size):
                if self.at(n) == color and n not in chain:
                    chain.add(n)
                    populate(n)

        chain.add(coord)
        populate(coord)
        return chain

    def chain_liberties(self, chain) -> set:
        libs = set()

        for c in chain:
            for n in neighbors(c, self.size):
                if self.at(n) == EMPTY:
                    libs.add(n)

        return libs

    def _add_move(self, move, caps=None):
        node = Node()
        node.action = NODE_BLACK if self.current == BLACK else NODE_WHITE
        node.move = move
        node.captures = list(caps) if caps else []

        self._add_node(node)

    def _add_node(self, node):
        node.id = len(self.tree)

        if self.current_node_id is not None:
            node.parent_id = self.current_node_id
            self.tree[node.parent_id].children.append(node.id)

        self.tree.append(node)
        self.current_node_id = node.id


def board_from_string(pos, size=9) -> Board:
    pos = re.sub(r'\s', '', pos)

    if len(pos) != size*size:
        raise ValueError('board string has incorrect length: {}'.format(len(pos)))

    board = Board(size)
    board.pos = list(pos)

    return board
