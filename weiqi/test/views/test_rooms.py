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

from weiqi.test.utils import get_json, login
from weiqi.test.factories import RoomFactory, RoomUserFactory


def test_room_users(app):
    ru = RoomUserFactory()

    res, data = get_json(app, '/api/rooms/'+str(ru.room.id)+'/users')

    assert res.status_code == 200
    assert data.get('users') is not None
    assert len(data.get('users')) == 1


def test_room_users_offline(app):
    room = RoomFactory()
    ru = RoomUserFactory(room=room, user__is_online=True)
    RoomUserFactory(room=room, user__is_online=False)
    ru2 = RoomUserFactory(room=room, user__is_online=True)

    res, data = get_json(app, '/api/rooms/'+str(room.id)+'/users')

    users = data.get('users')
    user_ids = [u['user_id'] for u in users]

    assert res.status_code == 200
    assert users is not None
    assert len(users) == 2
    assert ru.user_id in user_ids
    assert ru2.user_id in user_ids


def test_message(app):
    ru = RoomUserFactory()
    login(app, ru.user)

    res = app.post('/api/rooms/'+str(ru.room_id)+'/message', data={'message': 'test'})

    assert res.status_code == 200
    assert len(ru.room.messages) == 1


def test_message_not_in_room(app):
    room = RoomFactory()
    ru = RoomUserFactory()
    login(app, ru.user)

    res = app.post('/api/rooms/'+str(room.id)+'/message', data={'message': 'test'})

    assert res.status_code == 404
    assert len(ru.room.messages) == 0
    assert len(room.messages) == 0
