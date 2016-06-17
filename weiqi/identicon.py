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

import hashlib
import struct
from io import BytesIO

from PIL import Image, ImageDraw


def generate_identicon(data, size=256, cells=9):
    """Generates a symmetrical, random image based on the given data."""

    hs = hashlib.sha1()
    hs.update(data)
    hs = struct.unpack("Q", hs.digest()[:8])[0]

    color = (
        hs & 0xff,
        (hs >> 8) & 0xff,
        (hs >> 16) & 0xff,
    )
    hs >>= 24

    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    sq_size = size / (cells+1)
    border = (size - sq_size*cells) / 2

    for x in range(int((cells+1)/2)):
        for y in range(cells):
            if hs & 1 == 1:
                start_x = border + x*sq_size
                end_x = start_x + sq_size

                start_y = border + y*sq_size
                end_y = start_y + sq_size

                mirror_end_x = size - border - x*sq_size
                mirror_start_x = mirror_end_x - sq_size

                draw.rectangle(((start_x, start_y), (end_x, end_y)), fill=color)
                draw.rectangle(((mirror_start_x, start_y), (mirror_end_x, end_y)), fill=color)

            hs >>= 1

    del draw

    out = BytesIO()
    img.save(out, format='PNG')
    out.seek(0)

    return out
