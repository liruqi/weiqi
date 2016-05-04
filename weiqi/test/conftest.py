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

import pytest
from weiqi.message.pubsub import PubSub
from weiqi.message.broker import DummyBroker
from weiqi.handler.socket import SocketMixin
from weiqi.test import session
from weiqi.models import User, Room, RoomMessage, RoomUser, Connection, Automatch, Game


@pytest.fixture
def socket():
    socket = DummySocket()
    socket.initialize(PubSub(DummyBroker()))
    return socket


@pytest.fixture
def db():
    session.query(User).delete()
    session.query(RoomUser).delete()
    session.query(RoomMessage).delete()
    session.query(Connection).delete()
    session.query(Room).delete()
    session.query(User).delete()
    session.query(Automatch).delete()
    session.query(Game).delete()
    return session


class DummySocket(SocketMixin):
    def initialize(self, pubsub):
        super().initialize(pubsub)
        self.sent_messages = []
        self._compress = False

    def write_message(self, msg, *args, **kwargs):
        self.sent_messages.append(msg)
