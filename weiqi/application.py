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
import random
from datetime import timedelta

import tornado.httpserver
import tornado.options
import tornado.web
from tornado import gen
from weiqi import settings
from weiqi.db import session
from weiqi.handler import auth, socket, index, metrics
from weiqi.handler.socket import SocketMixin
from weiqi.message.broker import create_message_broker
from weiqi.message.pubsub import PubSub
from weiqi.services import GameService, PlayService


class Application(tornado.web.Application):
    def __init__(self):
        self.broker = create_message_broker()
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


def run_app(app, port):
    logging.info("Starting application ...")

    logging.info("Listening on :{}".format(port))
    app.listen(port, xheaders=True)

    spawn_cb = tornado.ioloop.IOLoop.current().spawn_callback
    spawn_cb(app.broker.run)
    spawn_cb(service_callback_runner(app, GameService, 'check_due_moves', timedelta(seconds=1)))
    spawn_cb(service_callback_runner(app, PlayService, 'cleanup_challenges', timedelta(seconds=1)))
    spawn_cb(service_callback_runner(app, PlayService, 'cleanup_automatches', timedelta(seconds=10)))

    tornado.ioloop.IOLoop.current().start()


def create_app():
    return Application()


def service_callback_runner(app, service, method, interval):
    """Returns a coroutine which periodically runs a method on the given service."""
    @gen.coroutine
    def callback():
        # Sleep for a random duration so that different processes don't all run at the same time.
        yield gen.sleep(random.random())

        while True:
            with session() as db:
                socket = SocketMixin()
                socket.initialize(app.pubsub)
                svc = service(db, socket)
                getattr(svc, method)()

            yield gen.sleep(interval.total_seconds())
    return callback
