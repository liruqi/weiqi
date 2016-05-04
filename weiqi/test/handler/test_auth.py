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

from weiqi.test.base import BaseAsyncHTTPTestCase
from weiqi.test import session
from weiqi.test.factories import RoomFactory
from weiqi.models import User
from weiqi.rating import min_rating


class TestSignUp(BaseAsyncHTTPTestCase):
    def test_sign_up(self):
        RoomFactory(is_default=False)
        room = RoomFactory(is_default=True)

        res = self.post('/api/auth/sign-up', {
            'display': 'display',
            'email': 'test@test.test',
            'rank': '3k',
            'password': 'pw',
        })
        self.assertEqual(res.code, 200)

        user = session.query(User).one()

        self.assertEqual(user.display, 'display')
        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.rating, min_rating('3k'))
        self.assertTrue(user.check_password('pw'))
        self.assertIsNotNone(user.rating_data)
        self.assertEqual(user.rating_data.rating, min_rating('3k'))

        self.assertEqual(len(user.rooms), 1)
        self.assertEqual(user.rooms[0].room_id, room.id)
