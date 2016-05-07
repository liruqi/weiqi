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
import uuid
from datetime import datetime
from weiqi import settings
from weiqi.db import session
from weiqi.services import ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService
from weiqi.models import User


class SocketMixin:
    def initialize(self, pubsub):
        self.id = str(uuid.uuid4())
        self.pubsub = pubsub
        self._subs = set()
        self._services = [ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService]
        self._compress = True

    def open(self):
        self._execute_service('connection', 'connect')

    def on_message(self, data):
        if self._compress:
            msg = json.loads(zlib.decompress(data).decode())
        else:
            msg = json.loads(data)

        service, method = msg.get('method').split('/', 1)

        res = self._execute_service(service, method, msg.get('data'))

        if msg.get('id') is not None:
            self._send_data({'method': 'response', 'id': msg.get('id'), 'data': res})

    def on_close(self):
        for topic in self._subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)

        self._execute_service('connection', 'disconnect')

    def subscribe(self, topic):
        if topic not in self._subs:
            self.pubsub.subscribe(topic, self._on_pubsub)
            self._subs.add(topic)

    def unsubscribe(self, topic):
        if topic in self._subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)
            self._subs.remove(topic)

    def is_subscribed(self, topic):
        return topic in self._subs

    def publish(self, topic, data):
        self.pubsub.publish(topic, data)

    def send(self, topic, data):
        self._send_data({'method': topic, 'data': data})

    def _send_data(self, data):
        message = data

        if self._compress:
            message = json.dumps(data)
            message = zlib.compress(message.encode())

        self.write_message(message, binary=self._compress)

    def _on_pubsub(self, topic, data):
        topic = topic.split('/')[0]
        self.send(topic, data)

    def _execute_service(self, service, method, data=None):
        service_names = {s.__service_name__: s for s in self._services}
        service_class = service_names.get(service)

        if not service_class:
            raise ValueError('service "{}" not found'.format(service))

        with session() as db:
            user = None
            user_id = self.get_secure_cookie(settings.COOKIE_NAME)

            if user_id:
                user = db.query(User).get(int(user_id))

            if user and method != 'ping':
                user.last_activity_at = datetime.utcnow()

            svc = service_class(db, self, user)
            return svc.execute(method, data)


class SocketHandler(SocketMixin, WebSocketHandler):
    pass
