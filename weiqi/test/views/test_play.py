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

from flask_login import current_user
import weiqi
from weiqi.models import Automatch, Game
from weiqi.test.utils import login
from weiqi.test.factories import UserFactory, AutomatchFactory


def test_automatch_inserting(app):
    user = UserFactory(rating=300)
    login(app, user)

    res = app.post('/api/play/automatch', data={'preset': 'fast', 'max_hc': 0})

    assert res.status_code == 200
    assert Automatch.query.count() == 1

    item = Automatch.query.first()
    assert item.user == current_user
    assert item.user_rating == current_user.rating
    assert item.preset == 'fast'
    assert item.min_rating == 300
    assert item.max_rating == 399


def test_automatch_create_game(app):
    user = UserFactory(rating=1500)
    other = UserFactory(rating=1600)
    AutomatchFactory(user=other, user_rating=1600, user__rating=1600, min_rating=1500, max_rating=1700)
    login(app, user)

    client = weiqi.socketio.test_client(weiqi.app)

    res = app.post('/api/play/automatch', data={'preset': 'fast', 'max_hc': 1})
    recv = client.get_received()

    assert res.status_code == 200
    assert Automatch.query.count() == 0
    assert Game.query.count() == 1

    game = Game.query.first()
    assert not game.is_demo
    assert game.is_ranked
    assert game.board is not None
    assert game.board.size == 9
    assert game.komi == 7.5
    assert game.stage == 'playing'
    assert len(game.room.users) == 2

    assert game.black_user in [user, other]
    assert game.white_user in [user, other]
    assert game.black_user != game.white_user

    assert game.black_display in [user.display, other.display]
    assert game.white_display in [user.display, other.display]
    assert game.black_display != game.white_display

    assert game.black_rating in [user.rating, other.rating]
    assert game.white_rating in [user.rating, other.rating]
    assert game.black_rating != game.white_rating

    assert len(recv) == 2
    assert recv[1]['name'] == 'game_started'
    assert recv[1]['args'][0] == game.to_frontend()
