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

from datetime import datetime

from weiqi import settings
from weiqi.models import Game, Room, User
from weiqi.services import BaseService


class DashboardService(BaseService):
    __service_name__ = 'dashboard'

    @BaseService.register
    def popular_games(self):
        games = (self.db.query(Game)
                 .join(Room)
                 .filter(Game.created_at >= datetime.utcnow() - settings.DASHBOARD_POPULAR_GAMES_MAX_AGE)
                 .filter(Game.is_private.is_(False))
                 .order_by(Room.users_max.desc())
                 .limit(settings.DASHBOARD_POPULAR_GAMES))

        return [g.to_frontend() for g in games]

    @BaseService.register
    def stats(self):
        users = self.db.query(User).count()
        online = self.db.query(User).filter_by(is_online=True).count()
        games = self.db.query(Game).count()

        return {
            'users': users,
            'online': online,
            'games': games
        }
