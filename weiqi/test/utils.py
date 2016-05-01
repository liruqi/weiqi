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

import json


def get_json(app, *args, **kwargs):
    res = app.get(*args, **kwargs)
    data = json.loads(res.data.decode())
    return res, data


def login(app, user, password='pw'):
    return app.post('/api/auth/sign-in', data={'email': user.email, 'password': password})


def logout(app):
    return app.get('/api/auth/logout')
