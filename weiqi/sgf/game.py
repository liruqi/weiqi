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

from weiqi.models import Game
from weiqi.board import Board, coord_from_sgf, BLACK, WHITE
from weiqi.sgf import parse_sgf


def game_from_sgf(sgf):
    node = parse_sgf(sgf)
    return game_from_node(node)


def game_from_node(node):
    game = Game(is_demo=True)
    game.board = Board(int(node.prop_one('SZ', '19')))
    game.komi = float(node.prop_one('KM', 6.5))
    game.result = node.prop_one('RE')
    game.black_display = node.prop_one('PB')
    game.white_display = node.prop_one('PW')
    game.title = node.prop_one('EV')

    _replay_game(game.board, node)

    if game.board.tree:
        game.board.current_node_id = 0

    return game


def _replay_game(board, node):
    if node.props.get('AB') or node.props.get('AW') or node.props.get('AE'):
        board.add_edits(_prop_coords(node.props.get('ab'), board.size),
                        _prop_coords(node.props.get('aw'), board.size),
                        _prop_coords(node.props.get('ae'), board.size))

    if node.prop_one('B'):
        board.current = BLACK
        board.play(coord_from_sgf(node.prop_one('B'), board.size))

    if node.prop_one('W'):
        board.current = WHITE
        board.play(coord_from_sgf(node.prop_one('W'), board.size))

    current_node_id = board.current_node_id

    for child in node.children:
        board.current_node_id = current_node_id
        _replay_game(board, child)


def _prop_coords(coords, size):
    if not coords:
        return []
    return [coord_from_sgf(c, size) for c in coords]
