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

import multiprocessing
import os.path
import tempfile

from selenium import webdriver
from tornado.testing import get_unused_port
from weiqi import settings
from weiqi.application import create_app, run_app
from weiqi.db import create_db, create_schema, session
from weiqi.models import User
from weiqi.services import RoomService


def _run_integration(port):
    with tempfile.TemporaryDirectory() as tmpdir:
        settings.DEBUG = False
        settings.LISTEN_PORT = port
        settings.DB_URL = 'sqlite:///' + os.path.join(tmpdir, 'weiqi.integration.db')
        settings.RECAPTCHA['backend'] = 'dummy'
        settings.MAILER['backend'] = 'console'

        create_db()
        create_schema()

        with session() as db:
            user = User(display='test', email='test@test.test')
            user.set_password('test')

            user2 = User(display='test', email='test2@test.test')
            user2.set_password('test2')

            db.add(user)
            db.add(user2)

            RoomService(db).create_default_room('Main')

        app = create_app()
        run_app(app, port)


def test_chat():
    port = get_unused_port()

    try:
        proc = multiprocessing.Process(target=_run_integration, args=(port,))
        proc.start()

        driver = webdriver.Chrome()

        host = 'http://localhost:' + str(port)
        driver.get(host)

        print(driver.find_element_by_xpath("//*[contains(text(), 'Sign in')]"))
    finally:
        proc.terminate()
        driver.close()
