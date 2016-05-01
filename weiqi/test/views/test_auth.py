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

from flask_login import current_user
from weiqi.models import User
from weiqi.rating import min_rating
from weiqi.test.factories import RoomFactory


def test_sign_up(app):
    RoomFactory(is_default=False)
    room = RoomFactory(is_default=True)

    app.post('/api/auth/sign-up', data={
        'display': 'name',
        'email': 'test@test.test',
        'password': 'test',
        'rank': '5k',
    })

    user = User.query.filter_by(email='test@test.test').first()

    assert user is not None
    assert user.display == 'name'
    assert user.email == 'test@test.test'
    assert user.check_password('test')
    assert user.rating == min_rating('5k')
    assert user.rating_data is not None
    assert user.rating_data.rating == min_rating('5k')

    assert len(user.rooms) == 1
    assert user.rooms[0].room_id == room.id

    assert current_user.is_authenticated
