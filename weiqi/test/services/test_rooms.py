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
from weiqi.test.factories import RoomFactory, RoomUserFactory
from weiqi.services import RoomService, ServiceError
from weiqi.models import User, RoomMessage


def test_room_users(db, socket):
    ru = RoomUserFactory()
    svc = RoomService(db, socket, ru.user)
    data = svc.execute('users', {'room_id': ru.room_id})

    assert data.get('users') is not None
    assert len(data.get('users')) == 1


def test_room_users_offline(db, socket):
    room = RoomFactory()
    ru = RoomUserFactory(room=room, user__is_online=True)
    RoomUserFactory(room=room, user__is_online=False)
    ru2 = RoomUserFactory(room=room, user__is_online=True)

    svc = RoomService(db, socket, ru.user)
    data = svc.execute('users', {'room_id': ru.room_id})

    users = data.get('users')
    user_ids = [u['user_id'] for u in users]

    assert users is not None
    assert len(users) == 2
    assert ru.user_id in user_ids
    assert ru2.user_id in user_ids


def test_message(db, socket):
    ru = RoomUserFactory()
    svc = RoomService(db, socket, ru.user)
    svc.execute('message', {'room_id': ru.room_id, 'message': 'test'})

    assert db.query(RoomMessage).count() == 1

    msg = db.query(RoomMessage).first()
    assert msg.message == 'test'
    assert msg.user == ru.user
    assert msg.room == ru.room


def test_message_not_in_room(db, socket):
    room = RoomFactory()
    ru = RoomUserFactory()

    svc = RoomService(db, socket, ru.user)

    with pytest.raises(ServiceError):
        svc.execute('message', {'room_id': room.id, 'message': 'test'})

    assert len(ru.room.messages) == 0
    assert len(room.messages) == 0
