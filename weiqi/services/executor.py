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

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from weiqi import metrics
from weiqi.db import session
from weiqi.models import User
from weiqi.services import (ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService,
                            DashboardService)

_executor = ThreadPoolExecutor(10)
_services = [ConnectionService, RoomService, GameService, PlayService, UserService, SettingsService, DashboardService]


def execute_service(socket, user_id, service_name, method, data):
    """Executes the given service method on a ThreadPoolExecutor and returns its `Future` object."""
    return _executor.submit(_execute_service, socket, service_name, method, data, user_id)


def _execute_service(socket, service, method, data, user_id):
    with metrics.EXCEPTIONS.labels(service+'/'+method).count_exceptions():
        with session() as db:
            user = db.query(User).get(user_id) if user_id else None

            service_names = {s.__service_name__: s for s in _services}
            service_class = service_names.get(service)

            if not service_class:
                raise ValueError('service "{}" not found'.format(service))

            if user and method != 'ping':
                user.last_activity_at = datetime.utcnow()

            svc = service_class(db, socket, user)
            return svc.execute(method, data)
