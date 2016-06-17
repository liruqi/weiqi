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
from weiqi.db import session
from weiqi.models import User


class BaseHandler(RequestHandler):
    def initialize(self, pubsub):
        self.pubsub = pubsub

    def get_current_user(self):
        id = self.get_secure_cookie(settings.COOKIE_NAME)

        if not id:
            return None

        if not self.db.query(User).get(int(id)):
            return None

        return int(id)

    def query_current_user(self):
        return self.db.query(User).get(self.current_user)

    def enable_cors(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", 'GET')

    def _execute(self, *args, **kwargs):
        with session() as db:
            self.db = db
            super()._execute(*args, **kwargs)
