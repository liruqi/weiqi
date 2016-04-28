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

import json
from collections import defaultdict


class PubSub:
    def __init__(self, broker):
        self._broker = broker
        self._broker.add_handler(self._on_message)

        self._subs = defaultdict(set)

    def _on_message(self, message):
        message = json.loads(message)
        topic = message.get('topic')
        data = message.get('data')

        for sub in self._subs[topic]:
            sub(topic, data)

    def publish(self, topic, data):
        message = json.dumps({
            'topic': topic,
            'data': data
        })

        self._broker.send_message(message)

    def subscribe(self, topic, handler):
        self._subs[topic].add(handler)

    def unsubscribe(self, topic, handler):
        self._subs[topic].remove(handler)

    def close(self):
        self._broker.remove_handler(self._on_message)
