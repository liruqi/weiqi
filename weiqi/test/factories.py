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
from weiqi.models import User, Room, RoomUser, Automatch, Game
from weiqi.board import Board
from weiqi.test import session
from weiqi.glicko2 import Player


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n)
    email = FuzzyText(suffix='@test.test')
    password = factory.PostGenerationMethodCall('set_password', 'pw')
    display = FuzzyText()
    is_online = True
    rating = 1000
    rating_data = factory.lazy_attribute(lambda o: Player(o.rating))


class RoomFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Room
        sqlalchemy_session = session
        force_flush = True

    id = factory.Sequence(lambda n: n)
    name = FuzzyText()
    type = 'main'
    is_default = True


class RoomUserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RoomUser
        sqlalchemy_session = session
        force_flush = True

    room = factory.SubFactory(RoomFactory)
    user = factory.SubFactory(UserFactory)

    has_unread = False


class AutomatchFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Automatch
        sqlalchemy_session = session
        force_flush = True

    user = factory.SubFactory(UserFactory, rating=1000)
    user_rating = factory.lazy_attribute(lambda o: o.user.rating)
    min_rating = 1000
    max_rating = 1099
    preset = 'fast'


class GameFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Game
        sqlalchemy_session = session
        force_flush = True

    room = factory.SubFactory(RoomFactory)
    is_demo = False
    is_ranked = True
    stage = 'playing'
    board = factory.lazy_attribute(lambda o: Board(9))
    komi = 7.5
    result = ''
    black_user = factory.SubFactory(UserFactory)
    black_display = factory.lazy_attribute(lambda o: o.black_user.display)
    black_rating = factory.lazy_attribute(lambda o: o.black_user.rating)
    white_user = factory.SubFactory(UserFactory)
    white_display = factory.lazy_attribute(lambda o: o.white_user.display)
    white_rating = factory.lazy_attribute(lambda o: o.white_user.rating)
