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

RATING_START = 100
RATING_PER_RANK = 100
MIN_RANK = -20
MAX_RANK = 9

DAN_SYMBOL = 'd'
KYU_SYMBOL = 'k'


def rating_to_rank(rating):
    rank = normalize(rating)

    if rank > 0:
        return str(rank)+DAN_SYMBOL

    return str(-rank)+KYU_SYMBOL


def normalize(rating):
    rank = MIN_RANK + int((rating-RATING_START)/RATING_PER_RANK)

    if rank >= 0:
        rank += 1  # Adjust for 1k/1d gap

    rank = min(MAX_RANK, rank)
    rank = max(MIN_RANK, rank)

    return rank


def rank_diff(rating, other):
    rnorm = normalize(rating)
    onorm = normalize(other)

    if rnorm > 0:
        rnorm -= 1
    if onorm > 0:
        onorm -= 1

    return abs(rnorm-onorm)


def min_rating(rank):
    if len(rank) < 2:
        raise ValueError('invalid rank: {}'.format(rank))

    symbol = rank[-1]
    number = int(rank[:-1])

    if symbol not in [DAN_SYMBOL, KYU_SYMBOL]:
        raise ValueError('invalid rank symbol: {}'.format(rank))

    if symbol == DAN_SYMBOL:
        number = min(MAX_RANK, number)
        return (abs(MIN_RANK)+number-1)*RATING_PER_RANK + RATING_START

    number = min(-MIN_RANK, number)
    return (abs(MIN_RANK)-number)*RATING_PER_RANK + RATING_START
