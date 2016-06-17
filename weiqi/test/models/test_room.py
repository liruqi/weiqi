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

from weiqi.test.factories import RoomFactory, RoomUserFactory, RoomMessageFactory


def test_room_recent_messages(db):
    room = RoomFactory()
    ru = RoomUserFactory(room=room)

    RoomMessageFactory(room=room,
                       user=ru.user,
                       message='new',
                       created_at=datetime(2016, 5, 23))

    RoomMessageFactory(room=room,
                       user=ru.user,
                       message='old',
                       created_at=datetime(2016, 5, 22))

    RoomMessageFactory(room=room,
                       user=ru.user,
                       message='even older',
                       created_at=datetime(2016, 5, 21))

    msg = list(room.recent_messages(db, 2))
    assert msg[0].message == 'old'
    assert msg[1].message == 'new'
