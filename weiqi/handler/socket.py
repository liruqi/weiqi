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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subs = set()

    def open(self):
        self._send_connection_data()
        self._subscribe('room_message')

    def on_message(self, message):
        pass

    def on_close(self):
        for topic in self.subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)

    def _subscribe(self, topic):
        if topic not in self.subs:
            self.pubsub.subscribe(topic, self._on_pubsub)
            self.subs.add(topic)

    def _unsubscribe(self, topic):
        if topic in self.subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)
            self.subs.remove(topic)

    def _on_pubsub(self, topic, data):
        self._send_message(topic, data)

    def _send_message(self, topic, data):
        message = {'method': topic, 'data': data}
        message = json.dumps(message)
        message = zlib.compress(message.encode())
        self.write_message(message, binary=True)

    def _send_connection_data(self):
        data = self._connection_data_rooms()

        if self.current_user:
            user = self.query_current_user()
            data['user_id'] = user.id
            data['user_display'] = user.display

        self._send_message('connection_data', data)

    def _connection_data_rooms(self):
        rooms = []
        logs = {}

        for room in self.db.query(Room):
            rooms.append(room.to_frontend())
            logs[room.id] = [m.to_frontend() for m in room.messages]

        return {'rooms': rooms, 'room_logs': logs}
