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

from weiqi.services import UserService
from weiqi.test.factories import UserFactory


def test_profile(db, socket):
    user = UserFactory(is_online=True)
    svc = UserService(db, socket)

    profile = svc.execute('profile', {'user_id': user.id})

    assert profile.get('id') == user.id
    assert profile.get('last_activity_at') == user.last_activity_at.isoformat()
    assert profile.get('is_online') == user.is_online
    assert profile.get('rating') == user.rating
    assert profile.get('display') == user.display
    assert profile.get('info_text_html') == user.info_text_html


def test_autocomplete(db, socket):
    UserFactory(display='t_one_t')
    UserFactory(display='name')
    UserFactory(display='some_one')

    svc = UserService(db, socket)

    users = svc.execute('autocomplete', {'query': 'one'})

    assert len(users) == 2
