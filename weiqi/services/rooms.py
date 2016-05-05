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

from sqlalchemy.orm import aliased
from weiqi import settings
from weiqi.services import BaseService, ServiceError
from weiqi.models import Room, RoomMessage, RoomUser, User


class RoomService(BaseService):
    __service_name__ = 'rooms'

    @BaseService.authenticated
    @BaseService.register
    def message(self, room_id, message):
        ru = self.db.query(RoomUser).filter_by(user=self.user, room_id=room_id).one()

        msg = RoomMessage(
            room=ru.room,
            user=self.user,
            user_display=self.user.display,
            user_rating=self.user.rating,
            message=message)

        self.db.add(msg)
        self.db.commit()

        if ru.room.type == 'direct':
            self._message_direct(ru, msg)
        else:
            self.socket.publish('room_message/'+str(room_id), msg.to_frontend())

    def _message_direct(self, ru, msg):
        other = self.db.query(RoomUser).filter((RoomUser.room_id == ru.room_id) &
                                               (RoomUser.user != self.user)).first()
        if other:
            other.has_unread = True
            self.socket.publish('direct_message/'+str(self.user.id), msg.to_frontend())
            self.socket.publish('direct_message/'+str(other.user_id), msg.to_frontend())

    @BaseService.register
    def users(self, room_id):
        room = self.db.query(Room).get(room_id)
        query = self.db.query(RoomUser).filter_by(room_id=room.id).join('user').filter_by(is_online=True)

        return {'users': [ru.to_frontend() for ru in query]}

    @BaseService.authenticated
    @BaseService.register
    def open_direct(self, user_id):
        if user_id == self.user.id:
            raise ServiceError('cannot open direct-chat with oneself')

        other = self.db.query(User).get(user_id)
        if not other:
            raise ServiceError('user not found')

        room = self._direct_room(self.user, other)
        ru = self.db.query(RoomUser).filter_by(room=room, user=self.user).first()
        self.db.commit()

        self.socket.subscribe('room_message/'+str(room.id))
        self.socket.subscribe('room_user/'+str(room.id))
        self.socket.subscribe('room_user_left/'+str(room.id))

        return {
            'other_user_id': other.id,
            'other_display': other.display,
            'is_online': other.is_online,
            'is_active': True,
            'has_unread': ru.has_unread,
            'room': room.to_frontend(),
            'room_logs': [m.to_frontend() for m in room.messages.limit(settings.ROOM_MESSAGES_LIMIT)]
        }

    def _direct_room(self, user, other):
        ru1 = aliased(RoomUser)
        ru2 = aliased(RoomUser)
        room = self.db.query(Room).join(ru1).join(ru2).filter(
            (Room.type == 'direct') &
            (ru1.user == user) &
            (ru2.user == other)).first()

        if not room:
            room = Room(type='direct')
            self.db.add(room)
            self.db.add(RoomUser(room=room, user=user))
            self.db.add(RoomUser(room=room, user=other))

        return room

    @BaseService.register
    def mark_read(self, room_id):
        if not self.user:
            return

        ru = self.db.query(RoomUser).filter_by(user=self.user, room_id=room_id).first()
        if not ru:
            return

        ru.has_unread = False
