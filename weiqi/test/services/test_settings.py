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

from weiqi.services import SettingsService
from weiqi.test.factories import UserFactory


def test_change_user_info(db, socket):
    user = UserFactory(correspondence_emails=False)
    svc = SettingsService(db, socket, user)

    svc.execute('save_user_info', {
        'email': 'new-test@test.test',
        'info_text': 'new text',
        'correspondence_emails': True
    })

    assert user.email == 'new-test@test.test'
    assert user.info_text == 'new text'
    assert user.correspondence_emails


def test_change_password(db, socket):
    user = UserFactory()
    svc = SettingsService(db, socket, user)

    svc.execute('change_password', {'password': 'newpw'})

    assert user.check_password('newpw')
