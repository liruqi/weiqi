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

from unittest import TestCase
import json
from weiqi import app, db
from weiqi.models import User, Room, RoomMessage, RoomUser, Connection


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.app.__enter__()

        RoomUser.query.delete()
        RoomMessage.query.delete()
        Connection.query.delete()
        Room.query.delete()
        User.query.delete()

        db.session.commit()

    def tearDown(self):
        self.app.__exit__(None, None, None)
        self.ctx.pop()

    def get_json(self, *args, **kwargs):
        res = self.app.get(*args, **kwargs)
        data = json.loads(res.data.decode())
        return res, data

    def login(self, user, password='pw'):
        return self.app.post('/api/auth/sign-in', data={'email': user.email, 'password': password})

    def logout(self):
        return self.app.get('/api/auth/logout')
