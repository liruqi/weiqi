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
from weiqi.models import Room
from weiqi.handler.base import BaseHandler


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
        data = self._connection_data_rooms()

        if self.current_user:
            user = self.query_current_user()
            data['user_id'] = user.display

        self.send_message('connection_data', data)

    def _connection_data_rooms(self):
        rooms = []
        logs = {}

        for room in self.db.query(Room):
            rooms.append(room.to_frontend())
            logs[room.id] = [m.to_frontend() for m in room.messages]

        return {'rooms': rooms, 'room_logs': logs}
