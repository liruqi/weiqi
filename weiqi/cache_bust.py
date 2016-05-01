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
import hashlib


def init_cache_buster(app):
    """Configure `app` so that `url_for` adds an additional query parameter as cache buster.

    The added query parameter is a hash based on the contents of the static file, making it possible to use long
    `max-age` values for Cache-Control.
    """

    version_cache = {}

    @app.url_defaults
    def append_hash(endpoint, values):
        if endpoint == 'static':
            path = os.path.join(app.static_folder, values['filename'])

            if path not in version_cache:
                version = get_file_version(path)
                version_cache[path] = version
            else:
                version = version_cache[path]

            values['v'] = version


def get_file_version(path):
    """Returns a version string for the given file."""

    hasher = hashlib.md5()

    with open(path, 'rb') as f:
        for chunk in f:
            hasher.update(chunk)

    return hasher.hexdigest().encode()
