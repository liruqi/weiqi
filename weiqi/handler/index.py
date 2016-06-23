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

from sqlalchemy.orm import undefer
from tornado.web import HTTPError
from weiqi import settings
from weiqi.handler.base import BaseHandler
from weiqi.identicon import generate_identicon
from weiqi.models import User, Game
from weiqi.sgf import game_to_sgf


class IndexHandler(BaseHandler):
    def get(self):
        conf = {
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA['public'],
            'DEFAULT_KOMI': settings.DEFAULT_KOMI,
            'HANDICAP_KOMI': settings.HANDICAP_KOMI,
        }

        self.set_secure_cookie(settings.COOKIE_NAME, self.get_secure_cookie(settings.COOKIE_NAME) or '')

        self.set_header('Cache-control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

        self.render('index.html', settings=conf)


class PingHandler(BaseHandler):
    def get(self):
        self.write('pong')


class AvatarHandler(BaseHandler):
    def get(self, user_id):
        want_large = self.get_argument('size', '') == 'large'

        user = self.db.query(User.avatar, User.avatar_large, User.display).filter_by(id=user_id).first()

        if user:
            avatar = user[1] if want_large else user[0]
            display = user[2]
        else:
            avatar, display = None, ''

        if not avatar:
            data = '{}-{}'.format(user_id, display).strip('-')
            size = 256 if want_large else 64
            avatar = generate_identicon(data.encode(), size=size).getvalue()

        self.set_header('Content-Type', 'image/png')
        self.set_header('Cache-control', 'max-age=' + str(3600*24))
        self.write(avatar)


class SgfHandler(BaseHandler):
    def get(self, game_id):
        game = self.db.query(Game).options(undefer('board')).get(game_id)

        if not game:
            raise HTTPError(404)

        filename = '%s-%s-%s.sgf' % (game.created_at.date().isoformat(), game.white_display, game.black_display)

        self.set_header('Content-Type', 'application/x-go-sgf; charset=utf-8')
        self.set_header('Content-Disposition', 'attachment; filename="%s"' % filename)

        self.enable_cors()

        self.write(game_to_sgf(game))
