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
from datetime import timedelta

BASE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

DEBUG = True

SECRET = b'j$\x1eM\xe2K\xda\xc0zndD\x80\x10\xc0\x8c\xba\xa1\xaeC\x01y\xe7\xe1'
COOKIE_NAME = 'weiqi'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')

LISTEN_PORT = 8000
DB_URL = 'postgresql://weiqi:6ff6zzHxLmuLMpyuRyMC@localhost/weiqi'
AMPQ_URL = 'amqp://guest:guest@127.0.0.1:5672/'

RECAPTCHA = {
    'backend': 'dummy',
    'secret': '',
    'public': '6LdrkiATAAAAAGL1iWz14Nu7-VigpAtqpYWmpD0y',
}

MAILER = {
    'backend': 'console',
    'from': 'no-reply@weiqi.gs',
    'smtp_host': '',
    'smtp_port': 587,
    'smtp_user': '',
    'smtp_password': '',
}

ROOM_MESSAGES_LIMIT = 30

RATING_PERIOD_DURATION = timedelta(days=1)
GAME_START_DELAY = timedelta(seconds=10)

DEFAULT_KOMI = 7.5
HANDICAP_KOMI = 0.5

AUTOMATCH_SIZE = 19
AUTOMATCH_PRESETS = {
    'fast': {
        'main': timedelta(minutes=5),
        'overtime': timedelta(seconds=10),
    },
    'medium': {
        'main': timedelta(minutes=10),
        'overtime': timedelta(seconds=20),
    },
    'slow': {
        'main': timedelta(minutes=15),
        'overtime': timedelta(seconds=30),
    },
}

DASHBOARD_POPULAR_GAMES = 5
DASHBOARD_POPULAR_GAMES_MAX_AGE = timedelta(days=7)

CHALLENGE_EXPIRATION = timedelta(minutes=5)

# Maintime to add to each player's clock after server downtime.
RESUME_TIMING_ADD_TIME = timedelta(minutes=1)

METRICS_COLLECTION_INTERVAL = timedelta(seconds=10)
