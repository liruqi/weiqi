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

import logging

from weiqi.db import session
from weiqi.models import Connection, Automatch, User
from weiqi.services import GameService


def prepare_startup():
    """Prepares the server state for a clean startup.

    This is usually called separately to clean up the database before starting any worker processes.
    """
    logging.info("Preparing for startup ...")
    _prepare_db()


def _prepare_db():
    """Cleans DB state before starting the server."""
    logging.info("Cleaning database ...")
    with session() as db:
        db.query(Connection).delete()
        db.query(Automatch).filter(Automatch.preset != 'correspondence').delete()
        db.query(User).update({'is_online': False})
        GameService(db).resume_all_games()
