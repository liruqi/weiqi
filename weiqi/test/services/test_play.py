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

from datetime import datetime
from weiqi import settings
from weiqi.services import PlayService
from weiqi.models import Automatch, Game
from weiqi.test.factories import UserFactory, AutomatchFactory, GameFactory


def test_automatch_inserting(db, socket):
    user = UserFactory(rating=300)
    socket.subscribe('automatch_status/'+str(user.id))

    svc = PlayService(db, socket, user)
    svc.execute('automatch', {'preset': 'fast', 'max_hc': 0})

    assert db.query(Automatch).count() == 1

    item = db.query(Automatch).first()
    assert item.user == user
    assert item.user_rating == user.rating
    assert item.preset == 'fast'
    assert item.min_rating == 300
    assert item.max_rating == 399

    assert len(socket.sent_messages) == 1
    assert socket.sent_messages[0]['method'] == 'automatch_status'
    assert socket.sent_messages[0]['data']['in_queue']


def test_automatch_twice(db, socket):
    user = UserFactory()
    svc = PlayService(db, socket, user)

    svc.execute('automatch', {'preset': 'fast', 'max_hc': 0})
    svc.execute('automatch', {'preset': 'medium', 'max_hc': 0})

    assert db.query(Automatch).count() == 1
    item = db.query(Automatch).first()
    assert item.user == user
    assert item.preset == 'medium'


def test_automatch_create_game(db, socket):
    user = UserFactory(rating=1500)
    other = UserFactory(rating=1600)
    AutomatchFactory(user=other, user_rating=1600, user__rating=1600, min_rating=1500, max_rating=1700)

    socket.subscribe('game_started')
    socket.subscribe('automatch_status/'+str(user.id))
    socket.subscribe('automatch_status/'+str(other.id))

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
    assert len(game.room.users.all()) == 2

    assert game.black_user in [user, other]
    assert game.white_user in [user, other]
    assert game.black_user != game.white_user

    assert game.black_display in [user.display, other.display]
    assert game.white_display in [user.display, other.display]
    assert game.black_display != game.white_display

    assert game.black_rating in [user.rating, other.rating]
    assert game.white_rating in [user.rating, other.rating]
    assert game.black_rating != game.white_rating

    assert (game.timing.start_at - (datetime.utcnow() + settings.GAME_START_DELAY)).total_seconds() < 1
    assert (game.timing.start_at - game.timing.timing_updated_at).total_seconds() < 1
    assert (game.timing.start_at - game.timing.next_move_at).total_seconds() < 1

    assert len(socket.sent_messages) == 3
    assert socket.sent_messages[0]['method'] == 'game_started'
    assert socket.sent_messages[0]['data'] == game.to_frontend()
    assert socket.sent_messages[1]['method'] == 'automatch_status'
    assert not socket.sent_messages[1]['data']['in_queue']
    assert socket.sent_messages[2]['method'] == 'automatch_status'
    assert not socket.sent_messages[2]['data']['in_queue']


def test_upload_sgf(db, socket):
    user = UserFactory()
    svc = PlayService(db, socket, user)

    game_id = svc.execute('upload_sgf', {'sgf': '(;B[dd]W[qq])'})
    game = db.query(Game).get(game_id)

    assert game is not None
    assert game.room is not None
    assert game.is_demo
    assert game.demo_owner == user
    assert game.demo_owner_rating == user.rating
    assert game.demo_owner_display == user.display
    assert game.demo_control == user
    assert game.demo_control_display == user.display


def test_create_demo(db, socket):
    user = UserFactory()
    svc = PlayService(db, socket, user)

    game_id = svc.execute('create_demo', {'title': 'test', 'size': 19})
    game = db.query(Game).get(game_id)

    assert game is not None
    assert game.room is not None
    assert game.is_demo
    assert game.title == 'test'
    assert game.demo_owner == user
    assert game.demo_owner_rating == user.rating
    assert game.demo_owner_display == user.display
    assert game.demo_control == user
    assert game.demo_control_display == user.display


def test_create_demo_from_game(db, socket):
    user = UserFactory()
    game = GameFactory()
    svc = PlayService(db, socket, user)

    demo_id = svc.execute('create_demo_from_game', {'game_id': game.id})
    demo = db.query(Game).get(demo_id)

    assert demo is not None
    assert demo.room is not None
    assert demo.is_demo
    assert demo.board.to_dict() == game.board.to_dict()
    assert demo.black_display == game.black_display
    assert demo.white_display == game.white_display
    assert demo.demo_owner == user
    assert demo.demo_owner_rating == user.rating
    assert demo.demo_owner_display == user.display
    assert demo.demo_control == user
    assert demo.demo_control_display == user.display