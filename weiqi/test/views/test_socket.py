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

from weiqi.test import BaseTestCase
from weiqi import app, socketio


class TestSocket(BaseTestCase):
    """Currently `test_client()` does not use `current_user` from Flask-Login, so tests are limited. See:
    https://github.com/miguelgrinberg/Flask-SocketIO/issues/231
    """
    def test_connection_data(self):
        client = socketio.test_client(app)
        recv = client.get_received()

        self.assertEqual(len(recv), 1)
        self.assertEqual(recv[0]['name'], 'connection_data')
