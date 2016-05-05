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

from weiqi.services import RatingService
from weiqi.test.factories import GameFactory
from weiqi.glicko2 import WIN, LOSS


def test_update_ratings(db):
    game = GameFactory(stage='finished', result='W+R', black_user__rating=1500, white_user__rating=1500)
    svc = RatingService(db)

    svc.update_ratings(game)

    assert len(game.black_user.rating_data.results) == 1
    assert game.black_user.rating_data.results[0].result == LOSS
    assert game.black_user.rating_data.results[0].almost_equals(game.white_user.rating_data)
    assert game.black_user.rating_data.rating == 1500
    assert game.black_user.rating < 1500

    assert len(game.white_user.rating_data.results) == 1
    assert game.white_user.rating_data.results[0].result == WIN
    assert game.white_user.rating_data.results[0].almost_equals(game.black_user.rating_data)
    assert game.white_user.rating_data.rating == 1500
    assert game.white_user.rating > 1500


def test_handicap_black_win(db):
    game_normal = GameFactory(stage='finished', result='B+R', black_user__rating=1500, white_user__rating=1500)
    game_hc = GameFactory(stage='finished', result='B+R', black_user__rating=1500, white_user__rating=1700)
    game_hc.board.handicap = 2
    game_hc.apply_board_change()

    svc = RatingService(db)
    svc.update_ratings(game_normal)
    svc.update_ratings(game_hc)

    assert game_normal.black_user.rating == game_hc.black_user.rating


def test_handicap_black_loss(db):
    game_normal = GameFactory(stage='finished', result='W+R', black_user__rating=1500, white_user__rating=1500)
    game_hc = GameFactory(stage='finished', result='W+R', black_user__rating=1500, white_user__rating=1700)
    game_hc.board.handicap = 2
    game_hc.apply_board_change()

    svc = RatingService(db)
    svc.update_ratings(game_normal)
    svc.update_ratings(game_hc)

    assert game_normal.black_user.rating == game_hc.black_user.rating


def test_handicap_white_win(db):
    game_normal = GameFactory(stage='finished', result='W+R', black_user__rating=1700, white_user__rating=1700)
    game_hc = GameFactory(stage='finished', result='W+R', black_user__rating=1500, white_user__rating=1700)
    game_hc.board.handicap = 2
    game_hc.apply_board_change()

    svc = RatingService(db)
    svc.update_ratings(game_normal)
    svc.update_ratings(game_hc)

    assert game_normal.white_user.rating == game_hc.white_user.rating


def test_handicap_white_loss(db):
    game_normal = GameFactory(stage='finished', result='B+R', black_user__rating=1700, white_user__rating=1700)
    game_hc = GameFactory(stage='finished', result='B+R', black_user__rating=1500, white_user__rating=1700)
    game_hc.board.handicap = 2
    game_hc.apply_board_change()

    svc = RatingService(db)
    svc.update_ratings(game_normal)
    svc.update_ratings(game_hc)

    assert game_normal.white_user.rating == game_hc.white_user.rating
