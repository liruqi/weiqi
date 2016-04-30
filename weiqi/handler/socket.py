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
from weiqi.models import User, Room, Connection
from weiqi.handler.base import BaseHandler


class SocketHandler(WebSocketHandler, BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subs = set()

    def open(self):
        self._send_connection_data()
        self._init_subs()
        self._create_connection()

    def on_message(self, message):
        pass

    def on_close(self):
        for topic in self.subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)

        self._delete_connection()

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

    def _create_connection(self):
        conn = Connection(ip=self.request.remote_ip, user_id=self.current_user)
        self.db.add(conn)
        self.db.commit()
        self._connection_id = conn.id
        self._update_status()

    def _delete_connection(self):
        if self._connection_id:
            self.db.query(Connection).filter_by(id=self._connection_id).delete()
            self.db.commit()
            self._update_status()

    def _update_status(self):
        if not self.current_user:
            return

        user = self.query_current_user()
        user.is_online = self.db.query(Connection).filter_by(user_id=self.current_user).exists()
        self.db.commit()

        for ru in user.rooms:
            if user.is_online:
                self.pubsub.publish('room_user', ru.to_frontend())
            else:
                self.pubsub.publish('room_user_left', ru.to_frontend())

    def _init_subs(self):
        self._subscribe('room_message')
        self._subscribe('room_user')
        self._subscribe('room_user_left')
        self._subscribe('automatch_status')
        self._subscribe('game_started')
        self._subscribe('game_finished')
        self._subscribe('game_data')
        self._subscribe('game_update')
        self._subscribe('load_direct_room')

    def _send_connection_data(self):
        user = None
        data = {}

        if self.current_user:
            user = self.query_current_user()
            data['user_id'] = user.id
            data['user_display'] = user.display

        data.update(self._connection_data_rooms(user))

        self._send_message('connection_data', data)

    def _connection_data_rooms(self, user):
        rooms = []
        logs = {}

        query = self.db.query(Room).filter_by(type='main')

        if user:
            query = query.join('users').filter_by(user_id=user.id)

        for room in query:
            rooms.append(room.to_frontend())
            logs[room.id] = [m.to_frontend() for m in room.messages]

        return {'rooms': rooms, 'room_logs': logs}
