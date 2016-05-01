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

from flask_script import Manager
from flask_migrate import MigrateCommand

from weiqi import app, init_app, socketio, db
from weiqi.models import Connection, Automatch

init_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    Connection.query.delete()
    Automatch.query.delete()
    db.session.commit()

    socketio.run(app, debug=app.config['DEBUG'])
