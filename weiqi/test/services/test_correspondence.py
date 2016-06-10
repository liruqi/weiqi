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

from weiqi.services import CorrespondenceService
from weiqi.test.factories import GameFactory


def test_correspondence_settings(db, socket, mails):
    game = GameFactory(is_correspondence=True,
                       black_user__correspondence_emails=False,
                       black_user__is_online=False,
                       white_user__correspondence_emails=True,
                       white_user__is_online=False)

    svc = CorrespondenceService(db, socket)
    svc.notify_automatch_started(game)

    assert len(mails) == 1
    assert mails[0]['to'] == game.white_user.email
