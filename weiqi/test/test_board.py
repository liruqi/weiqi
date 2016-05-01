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

import pytest
from weiqi.board import (Board, coord2d, coord_to_2d, BLACK, WHITE, NODE_BLACK, NODE_WHITE, board_from_string,
                         IllegalMoveError, PASS, RESIGN)


def test_coord_to_2d():
    coord = coord2d(4, 5, 9)
    x, y = coord_to_2d(coord, 9)
    assert x == 4
    assert y == 5


def test_from_string():
    board = board_from_string(
        '.........'
        '..x......'
        '.........'
        '.........'
        '.........'
        '.........'
        '.........'
        '.......o.'
        '.........')

    assert board.at(coord2d(3, 2)) == BLACK
    assert board.at(coord2d(8, 8)) == WHITE


def test_play():
    board = Board()

    assert board.current == BLACK
    board.play(coord2d(4, 4))

    assert board.current == WHITE
    board.play(coord2d(3, 3))

    assert board.current == BLACK
    board.play(coord2d(6, 6))

    assert board.at(coord2d(4, 4)) == BLACK
    assert board.at(coord2d(3, 3)) == WHITE
    assert board.at(coord2d(6, 6)) == BLACK


def test_play_node():
    board = Board()

    assert board.current_node_id is None

    board.play(coord2d(4, 4))
    assert board.current_node_id == 0
    assert board.current_node.parent_id is None
    assert board.current_node.children == []
    assert board.current_node.action == NODE_BLACK
    assert board.current_node.move == coord2d(4, 4)

    board.play(coord2d(5, 5))
    assert board.current_node.id == 1
    assert board.current_node.parent_id == 0
    assert board.current_node.children == []
    assert board.tree[0].children == [1]
    assert board.current_node.action == NODE_WHITE
    assert board.current_node.move == coord2d(5, 5)

    board.play(coord2d(6, 6))
    assert board.current_node_id == 2
    assert board.current_node.parent_id == 1
    assert board.current_node.children == []
    assert board.tree[0].children == [1]
    assert board.tree[1].children == [2]
    assert board.current_node.action == NODE_BLACK
    assert board.current_node.move == coord2d(6, 6)


def test_play_captures():
    board = board_from_string(
        '.........'
        '...xxx...'
        '....oox..'
        '..xoox...'
        '..xox....'
        '...x.....'
        '.........'
        '.........'
        '.........')

    board.current = BLACK
    board.play(coord2d(4, 3))

    expected = board_from_string(
        '.........'
        '...xxx...'
        '...x..x..'
        '..x..x...'
        '..x.x....'
        '...x.....'
        '.........'
        '.........'
        '.........')

    assert str(board) == str(expected)


def test_ko_rule():
    board = board_from_string(
        '.........'
        '.........'
        '...o.....'
        '..oxo....'
        '..x.x....'
        '...x.....'
        '.........'
        '.........'
        '.........')

    board.current = WHITE
    board.play(coord2d(4, 5))

    assert board.ko == coord2d(4, 4)

    with pytest.raises(IllegalMoveError):
        board.validate_legal(coord2d(4, 4))


def test_chain():
    board = board_from_string(
        '.........'
        '.........'
        '...oxo...'
        '...xoo...'
        '...xx....'
        '....x....'
        '...x.....'
        '.........'
        '.........')

    chains = [
        [coord2d(4, 4), {coord2d(4, 4), coord2d(4, 5), coord2d(5, 5), coord2d(5, 6)}],
        [coord2d(4, 3), {coord2d(4, 3)}],
        [coord2d(5, 3), {coord2d(5, 3)}],
        [coord2d(6, 3), {coord2d(6, 3), coord2d(6, 4), coord2d(5, 4)}],
        [coord2d(4, 7), {coord2d(4, 7)}],
    ]

    for c in chains:
        assert board.chain_at(c[0]) == c[1]


def test_loose_chain():
    pytest.skip('not implemented')


def test_chain_liberties():
    board = board_from_string(
        '.........'
        '.........'
        '...oxo...'
        '...xoo...'
        '...xx....'
        '....x....'
        '...x.....'
        '.........'
        '.........')

    assert len(board.chain_liberties(board.chain_at(coord2d(4, 4)))) == 6
    assert len(board.chain_liberties(board.chain_at(coord2d(5, 4)))) == 4


def test_suicide():
    board = board_from_string(
        '.x.......'
        'x........'
        '...x.....'
        '..x.x....'
        '...x.....'
        '.........'
        '.........'
        '.........'
        '.........')

    board.current = WHITE
    assert board.is_suicide(coord2d(1, 1))
    assert board.is_suicide(coord2d(4, 4))


def test_suicide_capture():
    board = board_from_string(
        '.xo......'
        'xo.......'
        '...xo....'
        '..x.xo...'
        '...xo....'
        '.........'
        '.........'
        '.........'
        '.........')

    board.current = WHITE
    assert not board.is_suicide(coord2d(1, 1))
    assert not board.is_suicide(coord2d(4, 4))


def test_pass():
    board = Board()
    board.play(PASS)

    assert board.tree[0].move == PASS
    assert board.current == WHITE


def test_both_passed():
    board = Board()
    assert not board.both_passed

    board.play(PASS)
    assert not board.both_passed

    board.play(PASS)
    assert board.both_passed


def test_mark_dead():
    pytest.skip('not implemented')


def test_toggle_marked_dead():
    pytest.skip('not implemented')


def test_place_hc():
    pytest.skip('not implemented')
