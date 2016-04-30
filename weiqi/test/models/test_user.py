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

from weiqi.test import BaseTestCase
from weiqi.models import User


class TestUser(BaseTestCase):
    def test_password(self):
        user = User()
        user.set_password('pw')

        self.assertNotEqual(user.password, 'pw')
        self.assertTrue(user.check_password('pw'))
        self.assertFalse(user.check_password('invalid'))