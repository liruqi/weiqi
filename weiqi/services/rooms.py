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

from weiqi.services import BaseService
from weiqi.models import Room, RoomMessage, RoomUser


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

        self.socket.publish('room_message/'+str(room_id), msg.to_frontend())

    @BaseService.register
    def users(self, room_id):
        room = self.db.query(Room).get(room_id)
        query = self.db.query(RoomUser).filter_by(room_id=room.id).join('user').filter_by(is_online=True)

        return {'users': [ru.to_frontend() for ru in query]}
