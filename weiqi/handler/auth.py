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
from weiqi import settings
from weiqi.handler.base import BaseHandler
from weiqi.models import User, RoomUser, Room
from weiqi.rating import min_rating
from weiqi.glicko2 import Player


class SignUpHandler(BaseHandler):
    def post(self):
        user = User(display=self.get_body_argument('display'),
                    email=self.get_body_argument('email'))

        user.set_password(self.get_body_argument('password'))
        self._sign_up_rating(user, self.get_body_argument('rank'))
        self._sign_up_rooms(user)

        self.db.add(user)

        self.db.commit()
        self.set_secure_cookie(settings.COOKIE_NAME, str(user.id))

        self.write({})

    def _sign_up_rating(self, user, rank):
        rating = min_rating(rank)

        if rating < min_rating('20k') or rating > min_rating('3d'):
            raise HTTPError(400, 'invalid rank')

        user.rating = rating
        user.rating_data = Player(rating)

    def _sign_up_rooms(self, user):
        for room in self.db.query(Room).filter_by(type='main', is_default=True):
            ru = RoomUser(user=user, room=room)
            self.db.add(ru)


class EmailExistsHandler(BaseHandler):
    def post(self):
        email = self.get_body_argument('email')
        exists = self.db.query(User).filter_by(email=email).count() > 0
        self.write('true' if exists else 'false')


class SignInHandler(BaseHandler):
    def post(self):
        email = self.get_body_argument('email')
        password = self.get_body_argument('password')

        user = self.db.query(User).filter_by(email=email).one()

        if not user.check_password(password):
            raise HTTPError(403, 'invalid username or password')

        self.set_secure_cookie(settings.COOKIE_NAME, str(user.id))
        self.write({})


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')
