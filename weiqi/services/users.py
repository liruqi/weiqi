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
from weiqi.models import Connection, User, Game


class UserService(BaseService):
    __service_name__ = 'users'

    def publish_status(self):
        if not self.user:
            return

        self.user.is_online = self.db.query(Connection).filter_by(user_id=self.user.id).count() > 0

        for ru in self.user.rooms:
            if self.user.is_online:
                self.socket.publish('room_user/'+str(ru.room_id), ru.to_frontend())
            else:
                self.socket.publish('room_user_left/'+str(ru.room_id), ru.to_frontend())

    @BaseService.register
    def email_exists(self, email):
        return self.db.query(User).filter_by(email=email).count() > 0

    @BaseService.register
    def profile(self, user_id):
        user = self.db.query(User).get(user_id)
        if not user:
            return {}

        return {
            'id': user_id,
            'created_at': user.created_at.isoformat(),
            'rating': user.rating,
            'display': user.display,
        }

    @BaseService.register
    def games(self, user_id):
        user = self.db.query(User).get(user_id)
        if not user:
            return []

        return [g.to_frontend() for g in user.games(self.db)]

    def publish_rating_update(self):
        if not self.user:
            return

        self.socket.publish('rating_update/'+str(self.user.id), {
            'rating': self.user.rating,
            'wins': Game.count_wins(self.db, self.user)
        })
