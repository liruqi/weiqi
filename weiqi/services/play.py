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

from datetime import datetime
import random
from weiqi import settings
from weiqi.services import BaseService, ServiceError
from weiqi.rating import rating_range, rank_diff
from weiqi.models import Automatch, Room, RoomUser, Game, Timing, User
from weiqi.board import Board
from weiqi.sgf import game_from_sgf


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
                game = self._create_automatch_game(self.user, other.user, preset)
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

    def _create_automatch_game(self, user, other, preset):
        black, white, handicap = self.game_players_handicap(user, other)
        board = Board(settings.AUTOMATCH_SIZE, handicap)
        komi = settings.DEFAULT_KOMI if handicap == 0 else settings.HANDICAP_KOMI

        room = Room(type='game')
        ru = RoomUser(room=room, user=black)
        ru2 = RoomUser(room=room, user=white)

        game = Game(room=room,
                    is_demo=False,
                    is_ranked=True,
                    board=board,
                    stage='playing',
                    komi=komi,
                    black_user=black,
                    black_display=black.display,
                    black_rating=black.rating,
                    white_user=white,
                    white_display=white.display,
                    white_rating=white.rating)

        timing_preset = settings.AUTOMATCH_PRESETS[preset]
        start_at = datetime.utcnow() + settings.GAME_START_DELAY

        timing = Timing(game=game,
                        system='fischer',
                        start_at=start_at,
                        timing_updated_at=start_at,
                        next_move_at=start_at,
                        main=timing_preset['main'],
                        overtime=timing_preset['overtime'],
                        black_main=timing_preset['main'],
                        black_overtime=timing_preset['overtime'],
                        white_main=timing_preset['main'],
                        white_overtime=timing_preset['overtime'])

        self.db.add(room)
        self.db.add(ru)
        self.db.add(ru2)
        self.db.add(game)
        self.db.add(timing)

        return game

    def game_players_handicap(self, user: User, other: User):
        handicap = rank_diff(user.rating, other.rating)

        if handicap == 0:
            if random.choice([0, 1]) == 0:
                black, white = user, other
            else:
                black, white = other, user
        elif user.rating > other.rating:
            black, white = other, user
        else:
            black, white = user, other

        return black, white, handicap

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
    def upload_sgf(self, sgf):
        game = game_from_sgf(sgf)

        room = Room(type='game')
        self.db.add(room)

        game.is_demo = True
        game.is_ranked = False
        game.stage = 'finished'
        game.demo_owner = self.user
        game.demo_owner_rating = self.user.rating
        game.demo_owner_display = self.user.display
        game.demo_control = self.user
        game.demo_control_display = self.user.display
        game.room = room
        self.db.add(game)

        self.db.commit()

        return game.id

    @BaseService.authenticated
    @BaseService.register
    def create_demo(self, title, size):
        room = Room(type='game')
        self.db.add(room)

        game = Game(is_demo=True,
                    is_ranked=False,
                    room=room,
                    title=title,
                    board=Board(int(size)),
                    komi=7.5,
                    stage='finished',
                    demo_owner=self.user,
                    demo_owner_display=self.user.display,
                    demo_owner_rating=self.user.rating,
                    demo_control=self.user,
                    demo_control_display=self.user.display)

        self.db.add(game)
        self.db.commit()

        return game.id

    @BaseService.authenticated
    @BaseService.register
    def create_demo_from_game(self, game_id):
        game = self.db.query(Game).get(game_id)
        if not game:
            raise ServiceError('game not found')

        room = Room(type='game')
        self.db.add(room)

        demo = Game(is_demo=True,
                    is_ranked=False,
                    room=room,
                    board=game.board,
                    komi=game.komi,
                    stage='finished',
                    black_display=game.black_display,
                    white_display=game.white_display,
                    demo_owner=self.user,
                    demo_owner_display=self.user.display,
                    demo_owner_rating=self.user.rating,
                    demo_control=self.user,
                    demo_control_display=self.user.display)

        self.db.add(demo)
        self.db.commit()

        return demo.id

    @BaseService.authenticated
    @BaseService.register
    def challenge(self):
        pass
