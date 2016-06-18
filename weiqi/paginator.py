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

import math


def paginate(query, limit, page=1):
    total_results = query.count()
    total_pages = max(1, math.ceil(total_results / limit))
    page = max(1, page)
    page = min(total_pages, page)

    return {
        'query': query.limit(limit).offset((page-1)*limit),
        'page': page,
        'total_pages': total_pages,
        'total_results': total_results
    }
