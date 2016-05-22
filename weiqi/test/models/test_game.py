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

from weiqi.models import Game
from weiqi.test.factories import UserFactory, GameFactory, DemoGameFactory, RoomUserFactory


def test_winner_loser():
    black = UserFactory()
    white = UserFactory()

    tests = [
        ['B+1.5', (black, white)],
        ['W+1.5', (white, black)],
        ['B+R', (black, white)],
        ['W+R', (white, black)],
        ['B+T', (black, white)],
        ['W+T', (white, black)],
    ]

    for t in tests:
        game = Game(black_user=black, white_user=white, result=t[0])
        assert game.winner_loser == t[1]


def test_active_games(db):
    g1 = GameFactory(stage='playing')
    g2 = GameFactory(stage='playing')
    RoomUserFactory(room=g1.room, user=g1.black_user)
    RoomUserFactory(room=g1.room, user=g1.white_user)
    RoomUserFactory(room=g2.room, user=g2.black_user)
    RoomUserFactory(room=g2.room, user=g2.white_user)

    assert Game.active_games(db).count() == 2


def test_active_games_demo(db):
    demo = DemoGameFactory(demo_owner__is_online=True)
    RoomUserFactory(room=demo.room, user=demo.demo_owner)
    assert Game.active_games(db).count() == 1


def test_active_games_demo_offline(db):
    demo = DemoGameFactory(demo_owner__is_online=False)
    RoomUserFactory(room=demo.room, user=demo.demo_owner)
    assert Game.active_games(db).count() == 0


def test_active_games_demo_not_in_room(db):
    DemoGameFactory(demo_owner__is_online=False)
    assert Game.active_games(db).count() == 0
