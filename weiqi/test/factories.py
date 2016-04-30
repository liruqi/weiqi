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

import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText
from weiqi.models import User, Room, RoomUser
from weiqi.db import session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = FuzzyText(suffix='@test.test')
    password = factory.PostGenerationMethodCall('set_password', 'pw')
    display = FuzzyText()
    is_online = True


class RoomFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Room

    id = factory.Sequence(lambda n: n)
    name = FuzzyText()
    type = 'main'


class RoomUserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RoomUser

    room = factory.SubFactory(RoomFactory)
    user = factory.SubFactory(UserFactory)

    has_unread = False


def setup_factories():
    factories = [UserFactory, RoomFactory, RoomUserFactory]

    with session() as db:
        for f in factories:
            f._meta.sqlalchemy_session = db
