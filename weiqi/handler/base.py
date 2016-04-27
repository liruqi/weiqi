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

from tornado.web import RequestHandler
from weiqi import settings
from weiqi.models import User


class BaseHandler(RequestHandler):
    def get_current_user(self):
        id = self.get_secure_cookie(settings.COOKIE_NAME)
        return int(id) if id else None

    def query_current_user(self, db):
        return db.query(User).filter(User.id == self.current_user).one()
