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


class SocketHandler(WebSocketHandler):
    def open(self):
        print('WebSocket opened')
        self.write_message({'method': 'ConnectionData', 'data': {}})

    def on_message(self, message):
        pass

    def on_close(self):
        print("WebSocket closed")

    def write_message(self, message, binary=True):
        super().write_message(zlib.compress(json.dumps(message).encode()), binary=True)
