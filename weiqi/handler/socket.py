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
import json
import uuid
import logging
from datetime import datetime
from weiqi import settings, metrics
from weiqi.db import session
from weiqi.services import (ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService,
                            DashboardService)
from weiqi.models import User


class SocketMixin:
    def initialize(self, pubsub):
        self.id = str(uuid.uuid4())
        self.pubsub = pubsub
        self._subs = set()
        self._services = [ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService,
                          DashboardService]

    def get_compression_options(self):
        return {}

    def open(self):
        self._execute_service('connection', 'connect')
        metrics.CONNECTED_SOCKETS.inc()

    def on_message(self, data):
        msg = json.loads(data)
        service, method = msg.get('method').split('/', 1)

        with metrics.REQUEST_TIME.labels(msg.get('method')).time():
            res = self._execute_service(service, method, msg.get('data'))

        if msg.get('id') is not None:
            self._send_data({'method': 'response', 'id': msg.get('id'), 'data': res},
                            response_to=msg.get('method'))

    def on_close(self):
        for topic in self._subs:
            self.pubsub.unsubscribe(topic, self._on_pubsub)

        self._execute_service('connection', 'disconnect')
        metrics.CONNECTED_SOCKETS.dec()

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

    def _send_data(self, data, response_to=''):
        method = data.get('method') if not response_to else 'response/' + response_to
        data = json.dumps(data)

        metrics.SENT_MESSAGES.labels(method).observe(len(data))

        self.write_message(data)

    def _on_pubsub(self, topic, data):
        topic = topic.split('/')[0]
        self.send(topic, data)

    def _execute_service(self, service, method, data=None):
        with metrics.EXCEPTIONS.labels(service+'/'+method).count_exceptions():
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
    def _execute_service(self, *args, **kwargs):
        try:
            return super()._execute_service(*args, **kwargs)
        except:
            logging.exception('service failed to execute')
