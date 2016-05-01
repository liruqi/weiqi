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

from weiqi import app
from . import auth, index, socket, rooms, play, games


app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(rooms.bp, url_prefix='/api/rooms')
app.register_blueprint(play.bp, url_prefix='/api/play')
app.register_blueprint(games.bp, url_prefix='/api/games')
