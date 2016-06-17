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

import os

from sqlalchemy.orm import scoped_session
from weiqi import settings
from weiqi.db import Session, create_db, create_schema

settings.DEBUG = False
settings.DB_URL = os.environ.get('WEIQI_TEST_DB', 'sqlite://')
settings.RECAPTCHA['backend'] = 'dummy'
settings.MAILER['backend'] = 'console'

create_db()
create_schema()

session = scoped_session(Session)

# Patch the `weiqi.db.sessions` contextmanager to use the same session as other parts of the testing framework, such as
# in factory boy.
# This is mainly used to test tornado request handlers.
from contextlib import contextmanager
@contextmanager
def _patched_session():
    yield session

from weiqi import db
db.session = _patched_session