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

from weiqi.services import ConnectionService
from weiqi.models import Automatch
from weiqi.test.factories import UserFactory, AutomatchFactory, RoomFactory, RoomUserFactory


def test_connect_subs(db, socket):
    user = UserFactory()

    svc = ConnectionService(db, socket, user)
    svc.execute('connect')

    assert socket.is_subscribed('game_started')
    assert socket.is_subscribed('game_finished')
    assert socket.is_subscribed('direct_message/'+str(user.id))
    assert socket.is_subscribed('automatch_status/'+str(user.id))
    assert socket.is_subscribed('challenges/'+str(user.id))


def test_connection_data_rooms(db, socket):
    room = RoomFactory(type='main')
    ru = RoomUserFactory(room=room)
    socket.subscribe('connection_data')

    svc = ConnectionService(db, socket, ru.user)
    svc.execute('connect')

    data = socket.sent_messages[0]['data']

    assert 'rooms' in data
    assert len(data['rooms']) == 1


def test_connection_data_automatch(db, socket):
    match = AutomatchFactory()
    socket.subscribe('connection_data')

    svc = ConnectionService(db, socket, match.user)
    svc.execute('connect')

    data = socket.sent_messages[0]['data']

    assert data['automatch']


def test_disconnect_automatch(db, socket):
    user = UserFactory()
    AutomatchFactory(user=user)

    svc = ConnectionService(db, socket, user)
    svc.execute('disconnect')

    assert db.query(Automatch).count() == 0


def test_disconnect_automatch_correspondence(db, socket):
    user = UserFactory()
    AutomatchFactory(user=user, preset='slow')
    AutomatchFactory(user=user, preset='correspondence')

    svc = ConnectionService(db, socket, user)
    svc.execute('disconnect')

    assert db.query(Automatch).count() == 1
    assert db.query(Automatch).filter_by(preset='correspondence').count() == 1
