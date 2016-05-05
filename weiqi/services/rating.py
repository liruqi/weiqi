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

from sqlalchemy.orm import undefer
from weiqi.services import BaseService
from weiqi.models import User
from weiqi.glicko2 import Result, WIN, LOSS
from weiqi.rating import RATING_PER_RANK, RATING_START


class RatingService(BaseService):
    def update_ratings(self, game):
        if not game.is_ranked or game.stage != 'finished':
            return

        winner, loser = game.winner_loser

        # `winner_hc` is the handicap relative to whether the winning player was black or white.
        winner_hc = game.board.handicap
        if winner != game.black_user:
            winner_hc = -winner_hc

        winner = self._user_for_update(winner.id)
        loser = self._user_for_update(loser.id)

        winner.rating_data.add_result(self._rating_to_result(loser.rating_data, -winner_hc, WIN))
        winner.apply_rating_data_change()

        loser.rating_data.add_result(self._rating_to_result(winner.rating_data, winner_hc, LOSS))
        loser.apply_rating_data_change()

        # Recalculate rating data of this period to get the current rating as it would be if
        # this was the end of the rating period.

        data = winner.rating_data.clone()
        data.update_rating()
        winner.rating = max(RATING_START, data.rating)

        data = loser.rating_data.clone()
        data.update_rating()
        loser.rating = max(RATING_START, data.rating)

    def _user_for_update(self, user_id):
        return self.db.query(User).options(undefer('rating_data')).with_for_update().get(user_id)

    def _rating_to_result(self, rating, increase_by_hc, result):
        return Result(result,
                      rating.rating + increase_by_hc*RATING_PER_RANK,
                      rating.deviation,
                      rating.volatility)
