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

import os.path

BASE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

DEBUG = True

SECRET_KEY = b'j$\x1eM\xe2K\xda\xc0zndD\x80\x10\xc0\x8c\xba\xa1\xaeC\x01y\xe7\xe1'

SQLALCHEMY_DATABASE_URI = 'postgresql://weiqi:6ff6zzHxLmuLMpyuRyMC@localhost/weiqi'
SQLALCHEMY_TRACK_MODIFICATIONS = False
