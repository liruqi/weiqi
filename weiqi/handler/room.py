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

from tornado.web import authenticated
from weiqi.handler.base import BaseHandler
from weiqi.models import Room, RoomMessage


class MessageHandler(BaseHandler):
    @authenticated
    def post(self, room_id):
        room = self.db.query(Room).get(room_id)
        user = self.query_current_user()
        msg = RoomMessage(room=room,
                          user=user,
                          user_display=user.display,
                          user_rating=user.rating,
                          message=self.get_body_argument('message'))

        self.db.add(msg)
        self.db.commit()

        self.pubsub.publish('room_message', msg.to_frontend())


class UsersHandler(BaseHandler):
    def get(self, room_id):
        room = self.db.query(Room).get(room_id)
        users = [ru.user.to_frontend() for ru in room.users]
        self.write({'users': users})


class MarkReadHandler(BaseHandler):
    def post(self):
        self.write('false')

