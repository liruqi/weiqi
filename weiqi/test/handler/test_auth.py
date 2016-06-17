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

from weiqi.models import User
from weiqi.rating import min_rating
from weiqi.test import session
from weiqi.test.base import BaseAsyncHTTPTestCase
from weiqi.test.factories import RoomFactory, UserFactory


class TestSignUp(BaseAsyncHTTPTestCase):
    def test_sign_up(self):
        RoomFactory(is_default=False)
        room = RoomFactory(is_default=True)

        res = self.post('/api/auth/sign-up', {
            'display': 'display',
            'email': 'test@test.test',
            'rank': '3k',
            'password': 'pw',
            'recaptcha': 'PASS'
        })
        self.assertEqual(res.code, 200)

        user = session.query(User).one()

        self.assertFalse(user.is_active)
        self.assertEqual(user.display, 'display')
        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.rating, min_rating('3k'))
        self.assertTrue(user.check_password('pw'))
        self.assertIsNotNone(user.rating_data)
        self.assertEqual(user.rating_data.rating, min_rating('3k'))

        self.assertEqual(len(user.rooms), 1)
        self.assertEqual(user.rooms[0].room_id, room.id)

    def test_sign_up_confirm(self):
        user = UserFactory(is_active=False)

        res = self.fetch('/api/auth/sign-up/confirm/%d/%s' % (user.id, user.auth_token()))
        session.commit()

        self.assertEqual(res.code, 200)
        self.assertTrue(user.is_active)


class TestSignIn(BaseAsyncHTTPTestCase):
    def test_sign_in(self):
        user = UserFactory(is_active=True)

        res = self.post('/api/auth/sign-in', {
            'email': user.email,
            'password': 'pw'
        })
        session.commit()

        self.assertEqual(res.code, 200)

    def test_sign_in_not_activated(self):
        user = UserFactory(is_active=False)

        res = self.post('/api/auth/sign-in', {
            'email': user.email,
            'password': 'pw'
        })
        session.commit()

        self.assertEqual(res.code, 403)


class TestPasswordReset(BaseAsyncHTTPTestCase):
    def test_password_reset(self):
        user = UserFactory()

        res = self.post('/api/auth/password-reset', {
            'email': user.email
        })

        self.assertEqual(res.code, 200)

    def test_password_reset_confirm(self):
        user = UserFactory()

        res = self.post('/api/auth/password-reset/confirm/%d/%s' % (user.id, user.auth_token()), {
            'password': 'newpw',
            'password-confirm': 'newpw'
        })
        session.commit()

        self.assertEqual(res.code, 200)
        self.assertTrue(user.check_password('newpw'))
