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

from .settings_base import *

try:
    # settings_local.py can override base settings, usually for development.
    from .settings_local import *
except ImportError:
    pass


# Settings can be loaded from an external file with the path given as environment variable.
# This is useful for deployment on servers.
if 'WEIQI_SETTINGS' in os.environ:
    import importlib.util
    spec = importlib.util.spec_from_file_location('weiqi.settings', os.environ['WEIQI_SETTINGS'])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    globals().update(mod.__dict__)
