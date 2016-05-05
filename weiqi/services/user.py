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
from weiqi.models import Connection


class UserService(BaseService):
    def publish_status(self):
        if not self.user:
            return

        self.user.is_online = self.db.query(Connection).filter_by(user_id=self.user.id).count() > 0

        for ru in self.user.rooms:
            if self.user.is_online:
                self.socket.publish('room_user/'+str(ru.room_id), ru.to_frontend())
            else:
                self.socket.publish('room_user_left/'+str(ru.room_id), ru.to_frontend())
