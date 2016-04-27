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

from tornado.websocket import WebSocketHandler
import zlib
import json
from weiqi.handler.base import BaseHandler
from weiqi.db import session


class SocketHandler(WebSocketHandler, BaseHandler):
    def open(self):
        self._send_connection_data()

    def on_message(self, message):
        pass

    def on_close(self):
        pass

    def send_message(self, method, data):
        message = {'method': method, 'data': data}
        message = json.dumps(message)
        message = zlib.compress(message.encode())
        self.write_message(message, binary=True)

    def _send_connection_data(self):
        data = {}

        with session() as db:
            if self.current_user:
                user = self.query_current_user(db)
                data['UserID'] = user.display

        self.send_message('connection_data', data)
