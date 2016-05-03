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
from weiqi import settings
from weiqi.db import session
from weiqi.services import ConnectionService
from weiqi.models import User


class SocketHandler(WebSocketHandler):
    def initialize(self, pubsub):
        self.id = str(uuid.uuid4())
        self.subs = set()
        self.pubsub = pubsub

    def open(self):
        self._execute_service('connection', 'connect')

    def on_message(self, message):
        pass

    def on_close(self):
        for topic in self.subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)

        self._execute_service('connection', 'disconnect')

    def subscribe(self, topic):
        if topic not in self.subs:
            self.pubsub.subscribe(topic, self._on_pubsub)
            self.subs.add(topic)

    def unsubscribe(self, topic):
        if topic in self.subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)
            self.subs.remove(topic)

    def publish(self, topic, data):
        self.pubsub.publish(topic, data)

    def send(self, topic, data):
        message = {'method': topic, 'data': data}
        message = json.dumps(message)
        message = zlib.compress(message.encode())
        self.write_message(message, binary=True)

    def _on_pubsub(self, topic, data):
        self.send(topic, data)

    def _execute_service(self, service, method, data=None):
        service_class = {
            'connection': ConnectionService,
        }.get(service)

        if not service:
            raise ValueError('service "{}" not found'.format(service))

        with session() as db:
            user = None
            user_id = self.get_secure_cookie(settings.COOKIE_NAME)

            if user_id:
                user = db.query(User).get(int(user_id))

            svc = service_class(db, self, user)
            svc.execute(method, data)
