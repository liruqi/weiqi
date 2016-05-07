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
from sqlalchemy.orm import undefer
from weiqi.handler.base import BaseHandler
from weiqi.models import User, Game
from weiqi.identicon import generate_identicon
from weiqi.sgf import game_to_sgf


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class PingHandler(BaseHandler):
    def get(self):
        self.write('pong')


class AvatarHandler(BaseHandler):
    def get(self, user_id):
        avatar = self.db.query(User.avatar).filter_by(id=user_id).scalar()

        if not avatar:
            avatar = generate_identicon(user_id.encode()).getvalue()

        self.set_header('Content-Type', 'image/png')
        self.write(avatar)


class SgfHandler(BaseHandler):
    def get(self, game_id):
        game = self.db.query(Game).options(undefer('board')).get(game_id)

        if not game:
            raise HTTPError(404)

        filename = '%s-%s-%s.sgf' % (game.created_at.date().isoformat(), game.white_display, game.black_display)

        self.set_header('Content-Type', 'application/x-go-sgf; charset=utf-8')
        self.set_header('Content-Disposition', 'attachment; filename="%s"' % filename)
        self.write(game_to_sgf(game))
