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
from weiqi.services import GameService, ServiceError
from weiqi.test.factories import GameFactory
from weiqi.board import BLACK, WHITE, EMPTY


def test_move(db, socket):
    game = GameFactory()

    svc = GameService(db, socket, game.black_user)
    svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == BLACK
    assert game.board.current == WHITE


def test_move_current_color(db, socket):
    game = GameFactory()
    svc = GameService(db, socket, game.white_user)

    with pytest.raises(ServiceError):
        svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == EMPTY


def test_move_finished(db, socket):
    game = GameFactory(stage='finished')
    svc = GameService(db, socket, game.black_user)

    with pytest.raises(ServiceError):
        svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == EMPTY
