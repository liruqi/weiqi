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

from weiqi.services import PlayService
from weiqi.models import Automatch, Game
from weiqi.test.factories import UserFactory, AutomatchFactory


def test_automatch_inserting(db, socket):
    user = UserFactory(rating=300)

    svc = PlayService(db, socket, user)
    svc.execute('automatch', {'preset': 'fast', 'max_hc': 0})

    assert db.query(Automatch).count() == 1

    item = db.query(Automatch).first()
    assert item.user == user
    assert item.user_rating == user.rating
    assert item.preset == 'fast'
    assert item.min_rating == 300
    assert item.max_rating == 399


def test_automatch_create_game(db, socket):
    user = UserFactory(rating=1500)
    other = UserFactory(rating=1600)
    AutomatchFactory(user=other, user_rating=1600, user__rating=1600, min_rating=1500, max_rating=1700)

    socket.subscribe('game_started')

    svc = PlayService(db, socket, user)
    svc.execute('automatch', {'preset': 'fast', 'max_hc': 1})

    assert db.query(Automatch).count() == 0
    assert db.query(Game).count() == 1

    game = db.query(Game).first()
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

    print(socket.sent_messages)
    assert len(socket.sent_messages) == 1
    assert socket.sent_messages[0]['method'] == 'game_started'
    assert socket.sent_messages[0]['data'] == game.to_frontend()
