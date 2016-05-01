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

import pytest
from weiqi import db
from weiqi.models import User, Room, RoomMessage, RoomUser, Connection


@pytest.fixture
def app(request):
    from weiqi import app
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()
    client.__enter__()

    RoomUser.query.delete()
    RoomMessage.query.delete()
    Connection.query.delete()
    Room.query.delete()
    User.query.delete()

    db.session.commit()

    def cleanup():
        client.__exit__(None, None, None)
        ctx.pop()

    request.addfinalizer(cleanup)
    return client
