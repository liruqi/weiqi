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

from weiqi.test.utils import login
from weiqi.test.factories import GameFactory
from weiqi.board import BLACK, WHITE, EMPTY


def test_move(app):
    game = GameFactory()
    login(app, game.black_user)

    res = app.post('/api/games/'+str(game.id)+'/move', data={'move': 30})

    assert res.status_code == 200
    assert game.board.at(30) == BLACK
    assert game.board.current == WHITE


def test_move_current_color(app):
    game = GameFactory()
    login(app, game.white_user)

    res = app.post('/api/games/'+str(game.id)+'/move', data={'move': 30})

    assert res.status_code == 403
    assert game.board.at(30) == EMPTY


def test_move_finished(app):
    game = GameFactory(stage='finished')
    login(app, game.black_user)

    res = app.post('/api/games/'+str(game.id)+'/move', data={'move': 30})

    assert res.status_code == 403
    assert game.board.at(30) == EMPTY