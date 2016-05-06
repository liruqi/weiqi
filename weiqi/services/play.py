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

from weiqi.services import BaseService
from weiqi.rating import rating_range
from weiqi.models import Automatch, Room, RoomUser, Game
from weiqi.board import Board


class PlayService(BaseService):
    __service_name__ = 'play'

    @BaseService.authenticated
    @BaseService.register
    def automatch(self, preset, max_hc):
        start, end = rating_range(self.user.rating, max_hc)
        game = None

        try:
            self.db.query(Automatch).filter_by(user=self.user).delete()

            query = self.db.query(Automatch).with_for_update()
            query = query.filter(Automatch.min_rating <= self.user.rating,
                                 Automatch.max_rating >= self.user.rating,
                                 Automatch.user_rating >= start,
                                 Automatch.user_rating <= end)
            query = query.order_by(Automatch.created_at)
            other = query.first()

            if other:
                game = self._create_game(self.user, other.user, preset, True)
                self.db.delete(other)
            else:
                item = Automatch(preset=preset,
                                 user=self.user,
                                 user_rating=self.user.rating,
                                 min_rating=start,
                                 max_rating=end)
                self.db.add(item)

            self.db.commit()
        except:
            self.db.rollback()
            raise

        if game:
            self._publish_game_started(game)
            self._publish_automatch(game.black_user, False)
            self._publish_automatch(game.white_user, False)
        else:
            self._publish_automatch(self.user, True)

    def _create_game(self, user, other, preset, ranked):
        room = Room(type='game')
        ru = RoomUser(room=room, user=user)
        ru2 = RoomUser(room=room, user=other)

        board = Board(9)

        game = Game(room=room,
                    is_demo=False,
                    is_ranked=ranked,
                    board=board,
                    stage='playing',
                    komi=7.5,
                    black_user=user,
                    black_display=user.display,
                    black_rating=user.rating,
                    white_user=other,
                    white_display=other.display,
                    white_rating=other.rating)

        self.db.add(room)
        self.db.add(ru)
        self.db.add(ru2)
        self.db.add(game)

        return game

    def _publish_game_started(self, game):
        self.socket.publish('game_started', game.to_frontend())

    @BaseService.authenticated
    @BaseService.register
    def cancel_automatch(self):
        self.db.query(Automatch).filter_by(user=self.user).delete()
        self._publish_automatch(self.user, False)

    def _publish_automatch(self, user, in_queue):
        self.socket.publish('automatch_status/'+str(user.id), {'in_queue': in_queue})

    @BaseService.authenticated
    @BaseService.register
    def upload_sgf(self):
        pass

    @BaseService.authenticated
    @BaseService.register
    def create_demo(self):
        pass

    @BaseService.authenticated
    @BaseService.register
    def challenge(self):
        pass
