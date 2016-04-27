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

from tornado.web import HTTPError
from weiqi.handler.base import BaseHandler
from weiqi import settings
from weiqi.db import session
from weiqi.models import User


class SignUpHandler(BaseHandler):
    def post(self):
        with session() as db:
            user = User(display=self.get_body_argument('username'),
                        email=self.get_body_argument('email'),
                        rating=100)

            user.set_password(self.get_body_argument('password'))

            db.add(user)

        self.write({})


class UserExistsHandler(BaseHandler):
    def post(self):
        self.write('false')


class EmailExistsHandler(BaseHandler):
    def post(self):
        self.write('false')


class SignInHandler(BaseHandler):
    def post(self):
        email = self.get_body_argument('user')
        password = self.get_body_argument('password')

        with session() as db:
            user = db.query(User).filter(User.email == email).one()

            if not user.check_password(password):
                raise HTTPError(403, 'invalid username or password')

            self.set_secure_cookie('weiqi', str(user.id))


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie(settings.COOKIE_NAME, None)