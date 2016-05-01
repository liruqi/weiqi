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

RATING_PER_RANK = 100
MIN_RANK = -20
MAX_RANK = 9
TOTAL_RANKS = abs(MIN_RANK) + MAX_RANK
RATING_START = 100
RATING_END = RATING_START + TOTAL_RANKS * RATING_PER_RANK

DAN_SYMBOL = 'd'
KYU_SYMBOL = 'k'


def rating_to_rank(rating):
    rank = MIN_RANK + int((rating-RATING_START)/RATING_PER_RANK)

    if rank >= 0:
        rank += 1  # Adjust for 1k/1d gap

    rank = min(MAX_RANK, rank)
    rank = max(MIN_RANK, rank)

    if rank > 0:
        return str(rank)+DAN_SYMBOL

    return str(-rank)+KYU_SYMBOL


def min_rating(rank):
    """Returns the minimum possible rating for a rank."""
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


def max_rating(rank):
    """Returns the maximum possible rating for a rank."""
    return min_rating(rank) + RATING_PER_RANK - 1


def normalize(rating):
    return min_rating(rating_to_rank(rating))


def rating_range(rating, max_ranks):
    """Returns a start/end range for which ratings are still within `max_ranks`."""
    norm = normalize(rating)
    start = norm - max_ranks*RATING_PER_RANK
    end = norm + (max_ranks+1)*RATING_PER_RANK - 1
    inf = 9999

    if start < RATING_START:
        start = -inf
    if end > RATING_END:
        end = inf

    return start, end


def rank_diff(rating, other):
    return int(abs(normalize(rating)-normalize(other)) / RATING_PER_RANK)
