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

from weiqi.sgf import Reader, parse_property_name, parse_property_value, parse_sgf, game_from_sgf
from weiqi.board import coord_from_sgf


def test_property_name():
    tests = [
        ['prop', 'prop'],
        ['prop[val]', 'prop']
    ]

    for t in tests:
        assert parse_property_name(Reader(t[0])) == t[1]


def test_property_value():
    tests = [
        ['[val]', 'val'],
        ['[val]rest', 'val'],
        ['[val\\]more]', 'val]more'],
        ['[val\\more]', 'val\\more'],
    ]

    for t in tests:
        assert parse_property_value(Reader(t[0])) == t[1]


def test_parse_sgf():
    node = parse_sgf('(;SZ[9]EV[event]KM[7.5];B[qd];W[dc];B[pq];W[dp])')

    assert node.prop_one('sz') == '9'
    assert node.prop_one('ev') == 'event'
    assert node.prop_one('km') == '7.5'

    moves = [
        ['B', 'qd'],
        ['W', 'dc'],
        ['B', 'pq'],
        ['W', 'dp'],
    ]

    for move in moves:
        assert len(node.children) == 1

        node = node.children[0]
        assert len(node.props) == 1
        assert node.prop_one(move[0]) == move[1]


def test_parse_variations():
    node = parse_sgf('(;B[qd](;W[dc];B[pq])(;W[dp];B[pp]))')

    assert node.prop_one('b') == 'qd'
    assert len(node.children) == 2

    assert node.children[0].prop_one('w') == 'dc'
    assert len(node.children[0].children) == 1
    assert node.children[0].children[0].prop_one('b') == 'pq'

    assert node.children[1].prop_one('w') == 'dp'
    assert len(node.children[1].children) == 1
    assert node.children[1].children[0].prop_one('b') == 'pp'


def test_game_info():
    game = game_from_sgf(
        """
        (;GM[1]FF[4]CA[UTF-8]AP[CGoban:3]ST[2]
        RU[Japanese]SZ[9]HA[2]KM[6.50]RE[B+R]EV[event]
        PW[White]PB[Black]AB[gc][cg]
        (;W[gg]
        ;B[ff])
        (;W[ee]
        ;B[gg]))
        """)

    assert game.result == 'B+R'
    assert game.black_display == 'Black'
    assert game.white_display == 'White'
    assert game.title == 'event'


def test_game_board():
    game = game_from_sgf(
        """
        (;GM[1]FF[4]CA[UTF-8]AP[CGoban:3]ST[2]
        RU[Japanese]SZ[9]HA[2]KM[6.50]
        PW[White]PB[Black]AB[gc][cg]
        (;W[gg]
        ;B[ff]
        ;W[dd])
        (;W[ee]
        ;B[gg]))
        """)

    assert len(game.board.tree) == 6
    assert game.board.current_node_id == 0
    assert len(game.board.current_node.children) == 2
    assert game.board.current_node.action == 'E'

    child = game.board.tree[game.board.current_node.children[0]]
    grand_child = game.board.tree[child.children[0]]
    assert child.action == 'W'
    assert child.move == coord_from_sgf('gg', game.board.size)
    assert grand_child.action == 'B'
    assert grand_child.move == coord_from_sgf('ff', game.board.size)

    child = game.board.tree[game.board.current_node.children[1]]
    grand_child = game.board.tree[child.children[0]]
    assert child.action == 'W'
    assert child.move == coord_from_sgf('ee', game.board.size)
    assert grand_child.action == 'B'
    assert grand_child.move == coord_from_sgf('gg', game.board.size)
