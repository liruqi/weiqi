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

from tornado.options import define, options
from tornado.autoreload import add_reload_hook
from weiqi import settings
from weiqi.db import create_db, session
from weiqi.prepare_startup import prepare_startup
from weiqi.application import run_app
from weiqi.models import Room, RoomUser, User


def main():
    define_options()
    options.parse_command_line()

    settings.LISTEN_PORT += options.port_offset

    create_db()

    if options.prepare_startup:
        prepare_startup()
    elif options.create_room:
        create_room(options.create_room)
    else:
        if settings.DEBUG:
            add_reload_hook(prepare_startup)
        run_app()


def define_options():
    define("prepare_startup", type=bool, default=None,
           help="Prepare for startup instead of running the application.")
    define("create_room", type=str, default=None,
           help="Create a new default chat room")

    define("port_offset", type=int, default=0, help="Offset to add to the port number")


def create_room(name):
    with session() as db:
        room = Room(type='main',
                    is_default=True,
                    name=name)
        db.add(room)

        for user_id in db.query(User.id):
            ru = RoomUser(room=room, user_id=user_id)
            db.add(ru)
