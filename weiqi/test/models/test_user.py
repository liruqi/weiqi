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

from datetime import datetime, timedelta

from weiqi.models import User


def test_password():
    user = User()
    user.set_password('pw')

    assert user.password != 'pw'
    assert user.check_password('pw')
    assert not user.check_password('invalid')


def test_auth_token():
    user = User()
    user.set_password('pw')

    token = user.auth_token()
    assert token
    assert user.check_auth_token(token)
    assert not user.check_auth_token('00000-'+token.split('-')[1])


def test_auth_token_expired():
    user = User()
    user.set_password('pw')

    token = user.auth_token(str(datetime.timestamp(datetime.utcnow() - timedelta(days=29))))
    assert user.check_auth_token(token)

    token = user.auth_token(str(datetime.timestamp(datetime.utcnow() - timedelta(days=31))))
    assert not user.check_auth_token(token)
