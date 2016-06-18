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

from tornado.web import HTTPError


class ServiceError(Exception):
    pass


class BaseService:
    _methods = {}

    def __init__(self, db=None, socket=None, user=None):
        self.db = db
        self.socket = socket
        self.user = user

    @classmethod
    def register(cls, func):
        """Registers a method to be used via the `execute` method."""
        cls._methods[func.__qualname__] = func
        return func

    @classmethod
    def authenticated(cls, func):
        def inner(self, *args, **kwargs):
            if not self.user:
                raise HTTPError(403)
            return func(self, *args, **kwargs)
        return inner

    def execute(self, method, data=None):
        """Executes the given method on this class.

        The method name has to be registered via the `register` decorator.
        """
        method = self.__class__.__name__ + '.' + method

        if method not in self._methods:
            raise ServiceError('invalid method "{}"'.format(method))

        return self._methods[method](self, **(data or {}))
