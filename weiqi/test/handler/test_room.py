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

import json
from weiqi.test.base import BaseAsyncHTTPTestCase
from weiqi.test.factories import RoomFactory, RoomUserFactory


class TestRoomUsers(BaseAsyncHTTPTestCase):
    def test_room_users(self):
        ru = RoomUserFactory()

        res = self.fetch('/api/rooms/'+str(ru.room.id)+'/users')
        data = json.loads(res.body.decode())

        self.assertEqual(res.code, 200)
        self.assertIsNotNone(data.get('users'))
        self.assertEqual(len(data.get('users')), 1)

    def test_room_users_offline(self):
        room = RoomFactory()
        ru = RoomUserFactory(room=room, user__is_online=True)
        RoomUserFactory(room=room, user__is_online=False)
        ru2 = RoomUserFactory(room=room, user__is_online=True)

        res = self.fetch('/api/rooms/'+str(room.id)+'/users')
        data = json.loads(res.body.decode())
        users = data.get('users')
        user_ids = [u['id'] for u in users]

        self.assertEqual(res.code, 200)
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 2)
        self.assertIn(ru.user_id, user_ids)
        self.assertIn(ru2.user_id, user_ids)
