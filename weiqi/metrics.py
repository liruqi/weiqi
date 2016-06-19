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

from prometheus_client import Summary, Gauge, Counter


REQUEST_TIME = Summary('weiqi_request_processing_seconds', 'Time spent processing requests', ['method'])
SENT_MESSAGES = Summary('weiqi_sent_message_bytes', 'Size of outgoing messages', ['method'])
CONNECTED_SOCKETS = Gauge('weiqi_connected_sockets', 'Number of connected websockets')
EXCEPTIONS = Counter('weiqi_exceptions_total', 'Number of exceptions in requests', ['method'])
REGISTRATIONS = Counter('weiqi_registrations_total', 'Total number of registrations')
