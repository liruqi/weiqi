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

import bleach
import markdown


def markdown_to_html(text):
    """Converts the given text from markdown to html.

    Note that this function will only sanitize the html after conversion. This means that html from the input text
    will not be escaped unless it is deemed unsafe.
    """
    text = markdown.markdown(text)

    allowed_tags = bleach.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'p']
    text = bleach.clean(text, allowed_tags)

    return text
