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

from weiqi import settings
from weiqi.mailer import send_mail
from weiqi.services import BaseService


class CorrespondenceService(BaseService):
    def notify_automatch_started(self, game):
        if not game.is_correspondence:
            return

        for user, other in self._both_self_other(game):
            self._mail_if_offline(user,
                                  'Correspondence game started',
                                  'correspondence/automatch_started.txt',
                                  {'url': self._game_url(game), 'opponent': other.display})

    def notify_challenge_started(self, game):
        if not game.is_correspondence:
            return

        for user, other in self._both_self_other(game):
            self._mail_if_offline(user,
                                  'Correspondence game started',
                                  'correspondence/challenge_started.txt',
                                  {'url': self._game_url(game), 'opponent': other.display})

    def notify_move_played(self, game, played_by):
        if not game.is_correspondence:
            return

        other = (game.black_user if played_by == game.white_user else game.white_user)

        self._mail_if_offline(other,
                              'Correspondence move played',
                              'correspondence/move_played.txt',
                              {'url': self._game_url(game), 'opponent': played_by.display})

    def notify_game_finished(self, game):
        if not game.is_correspondence:
            return

        for user, other in self._both_self_other(game):
            self._mail_if_offline(user,
                                  'Correspondence game finished',
                                  'correspondence/game_finished.txt',
                                  {'url': self._game_url(game), 'opponent': other.display, 'result': game.result})

    def _mail_if_offline(self, user, subject, template, context):
        if user.correspondence_emails and not user.is_online:
            send_mail(user.email, user.display, subject, template, context)

    def _both_self_other(self, game):
        return (game.black_user, game.white_user), (game.white_user, game.black_user)

    def _game_url(self, game):
        return settings.BASE_URL + '/games/' + str(game.id)
