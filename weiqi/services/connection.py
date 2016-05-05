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

from weiqi.services import BaseService, UserService
from weiqi.models import Game, Room, RoomUser, Connection
from weiqi import settings


class ConnectionService(BaseService):
    __service_name__ = 'connection'

    @BaseService.register
    def connect(self):
        self.socket.send('connection_data', self._connection_data())

        self.socket.subscribe('game_started')
        self.socket.subscribe('game_finished')

        if self.user:
            self.socket.subscribe('direct_message/'+str(self.user.id))

        self._join_open_rooms_and_games()
        self._insert_connection()
        UserService(self.db, self.socket, self.user).publish_status()

    @BaseService.register
    def disconnect(self):
        self._delete_connection()
        UserService(self.db, self.socket, self.user).publish_status()

    @BaseService.register
    def open_game(self, game_id):
        game = self.db.query(Game).get(game_id)
        self.socket.subscribe('game/'+str(game_id))
        self._join_room_user(game.room_id)
        self.socket.send('game_data', game.to_frontend(full=True))

    def _connection_data(self):
        data = {}

        if self.user:
            data.update({
                'user_id': self.user.id,
                'user_display': self.user.display,
                'rating': self.user.rating,
            })

        data.update(self._connection_data_rooms())
        data.update(self._connection_data_games())
        data.update(self._connection_data_direct_rooms())

        return data

    def _connection_data_rooms(self):
        rooms = []
        logs = {}

        for room in Room.open_rooms(self.db, self.user):
            rooms.append(room.to_frontend())
            logs[room.id] = [m.to_frontend() for m in room.messages]

        return {'rooms': rooms, 'room_logs': logs}

    def _connection_data_games(self):
        if not self.user:
            return {}

        return {
            'open_games': [g.to_frontend(full=True) for g in self.user.open_games(self.db)]
        }

    def _connection_data_direct_rooms(self):
        if not self.user:
            return {}

        direct = []

        query = self.db.query(RoomUser).join(Room)
        query = query.filter((Room.type == 'direct') & (RoomUser.user == self.user))
        query = query.limit(settings.DIRECT_ROOMS_LIMIT)

        for ru in query:
            other = self.db.query(RoomUser).filter((RoomUser.room_id == ru.room_id) &
                                                   (RoomUser.user != self.user)).first()
            direct.append({
                'other_user_id': other.user_id,
                'other_display': other.user.display,
                'is_online': other.user.is_online,
                'is_active': True,
                'has_unread': ru.has_unread,
                'room': ru.room.to_frontend(),
                'room_logs': [m.to_frontend() for m in ru.room.messages.limit(settings.ROOM_MESSAGES_LIMIT)]
            })

        return {'direct_rooms': direct}

    def _join_open_rooms_and_games(self):
        for room in Room.open_rooms(self.db, self.user):
            self.socket.subscribe('room_message/'+str(room.id))
            self.socket.subscribe('room_user/'+str(room.id))
            self.socket.subscribe('room_user_left/'+str(room.id))

            if room.type == 'game':
                self.socket.subscribe('game_data/'+str(room.games[0].id))
                self.socket.subscribe('game_update/'+str(room.games[0].id))

    def _join_room_user(self, room_id):
        self.socket.subscribe('room/'+str(room_id))

        if self.user:
            if self.db.query(RoomUser).filter_by(room_id=room_id, user=self.user).count() == 0:
                self.db.add(RoomUser(room_id=room_id, user=self.user))

    def _insert_connection(self):
        conn = Connection(id=self.socket.id,
                          user=self.user,
                          ip=self.socket.request.remote_ip)

        self.db.add(conn)

    def _delete_connection(self):
        self.db.query(Connection).filter_by(id=self.socket.id).delete()
