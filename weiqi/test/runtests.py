#!/usr/bin/env python3
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

import unittest
import tornado.testing
import os.path
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)

sys.path.append(BASE_DIR)


def all():
    return unittest.defaultTestLoader.discover(os.path.join(BASE_DIR, 'weiqi', 'test'), pattern='*.py')


def main():
    from weiqi import settings
    from weiqi.db import create_db

    settings.DB_URL = 'sqlite://'
    create_db()

    tornado.testing.main()


if __name__ == '__main__':
    main()
