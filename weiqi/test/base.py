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

import urllib.parse
from unittest import TestCase

from tornado.testing import AsyncHTTPTestCase
from weiqi.application import create_app
from weiqi.models import User, RoomMessage, RoomUser, Room, DirectRoom, Connection, Automatch, Game, Timing, Challenge
from weiqi.test import session


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()

        session.rollback()
        session.query(RoomUser).delete()
        session.query(RoomMessage).delete()
        session.query(Connection).delete()
        session.query(DirectRoom).delete()
        session.query(Automatch).delete()
        session.query(Timing).delete()
        session.query(Game).delete()
        session.query(Room).delete()
        session.query(Challenge).delete()
        session.query(User).delete()


class BaseAsyncHTTPTestCase(BaseTestCase, AsyncHTTPTestCase):
    def get_app(self):
        return create_app()

    def post(self, url, data):
        return self.fetch(url, method='POST', body=urllib.parse.urlencode(data))
