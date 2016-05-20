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
from tornado.testing import AsyncHTTPTestCase
import urllib.parse
from weiqi.db import session
from weiqi.application import create_app
from weiqi.models import User, RoomMessage, RoomUser, Room, Connection, Automatch, Game, Timing


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()

        with session() as db:
            db.query(User).delete()
            db.query(RoomUser).delete()
            db.query(RoomMessage).delete()
            db.query(Connection).delete()
            db.query(Room).delete()
            db.query(User).delete()
            db.query(Automatch).delete()
            db.query(Game).delete()
            db.query(Timing).delete()


class BaseAsyncHTTPTestCase(BaseTestCase, AsyncHTTPTestCase):
    def get_app(self):
        return create_app()

    def post(self, url, data):
        return self.fetch(url, method='POST', body=urllib.parse.urlencode(data))
