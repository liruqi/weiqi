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

import logging
import tornado.web
import tornado.options
import tornado.httpserver
from weiqi import settings
from weiqi.handler import auth, socket, index, metrics
from weiqi.message.pubsub import PubSub
from weiqi.message.broker import Ampq
from weiqi.services import GameService, PlayService


class Application(tornado.web.Application):
    def __init__(self):
        self.broker = Ampq(settings.AMPQ_URL)
        self.pubsub = PubSub(self.broker)

        def handler(route, cls):
            return route, cls, dict(pubsub=self.pubsub)

        handlers = [
            handler(r'/api/ping', index.PingHandler),
            handler(r'/api/socket', socket.SocketHandler),
            handler(r'/api/auth/sign-up', auth.SignUpHandler),
            handler(r'/api/auth/sign-up/confirm/(.*?)/(.*?)', auth.SignUpConfirmHandler),
            handler(r'/api/auth/sign-in', auth.SignInHandler),
            handler(r'/api/auth/logout', auth.LogoutHandler),
            handler(r'/api/auth/password-reset', auth.PasswordResetHandler),
            handler(r'/api/auth/password-reset/confirm/(.*?)/(.*?)', auth.PasswordResetConfirmHandler),

            handler(r'/api/users/(.*?)/avatar', index.AvatarHandler),
            handler(r'/api/games/(.*?)/sgf', index.SgfHandler),

            handler(r'/api/metrics', metrics.MetricsHandler),

            handler(r'.*', index.IndexHandler),
        ]

        super().__init__(
            handlers,
            debug=settings.DEBUG,
            autoreload=settings.DEBUG,
            cookie_secret=settings.SECRET,
            template_path=settings.TEMPLATE_PATH,
            static_path=settings.STATIC_PATH)


def run_app():
    logging.info("Starting application ...")
    app = create_app()

    logging.info("Listening on :{}".format(settings.LISTEN_PORT))
    app.listen(settings.LISTEN_PORT, xheaders=True)

    tornado.ioloop.IOLoop.current().spawn_callback(app.broker.run)
    tornado.ioloop.IOLoop.current().spawn_callback(GameService.run_time_checker, app.pubsub)
    tornado.ioloop.IOLoop.current().spawn_callback(PlayService.run_challenge_cleaner, app.pubsub)
    tornado.ioloop.IOLoop.current().start()


def create_app():
    return Application()
