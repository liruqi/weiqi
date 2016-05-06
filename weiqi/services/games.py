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
from contextlib import contextmanager
from weiqi.db import transaction
from weiqi.services import BaseService, ServiceError, UserService, RatingService, RoomService
from weiqi.models import Game
from weiqi.board import RESIGN
from weiqi.scoring import count_score


class InvalidPlayerError(ServiceError):
    pass


class InvalidStageError(ServiceError):
    pass


class GameService(BaseService):
    __service_name__ = 'games'

    @BaseService.register
    def open_game(self, game_id):
        game = self.db.query(Game).get(game_id)
        if not game:
            return

        RoomService(self.db, self.socket, self.user).join_room(game.room_id)

        self.socket.subscribe('game_data/'+str(game_id))
        self.socket.subscribe('game_update/'+str(game_id))
        self.socket.send('game_data', game.to_frontend(full=True))

    @BaseService.register
    def close_game(self, game_id):
        game = self.db.query(Game).get(game_id)
        if not game:
            return

        RoomService(self.db, self.socket, self.user).leave_room(game.room_id)
        self.socket.unsubscribe('game_data/'+str(game_id))
        self.socket.unsubscribe('game_update/'+str(game_id))

    @BaseService.authenticated
    @BaseService.register
    def move(self, game_id, move):
        with self._game_for_update(game_id) as game:
            if game.is_demo:
                self._game_move_demo(game, move)
            else:
                self._game_move(game, move)

                if game.stage == 'finished':
                    self._finish_game(game)

            game.apply_board_change()

            self.db.commit()
            self._publish_game_update(game)

    @contextmanager
    def _game_for_update(self, game_id):
        with transaction(self.db):
            game = self.db.query(Game).options(undefer('board')).with_for_update().get(game_id)
            yield game

    def _game_move_demo(self, game, move):
        pass

    def _game_move(self, game, move):
        if self.user not in [game.black_user, game.white_user]:
            raise InvalidPlayerError()

        if game.stage == 'finished':
            raise InvalidStageError()

        # TODO: timing
        # if not game.timing.has_started:
        #   pass

        if move == RESIGN:
            self._resign(game)
            return

        if game.stage != 'playing':
            raise InvalidStageError()

        if game.current_user != self.user:
            raise InvalidPlayerError()

        # TODO: timing
        # if not game.timing.move_played(game.board.current):
        #   ... win by time ...

        game.board.play(move)

        if game.board.both_passed:
            game.stage = 'counting'
            self._update_score(game)

    def _resign(self, game):
        game.stage = 'finished'

        if self.user == game.black_user:
            game.result = 'W+R'
        elif self.user == game.white_user:
            game.result = 'B+R'
        else:
            raise InvalidPlayerError()

    def _update_score(self, game):
        score = count_score(game.board, game.komi)
        game.result = score.result
        game.board.current_node.score_points = score.points

    def _publish_game_update(self, game):
        self.socket.publish('game_update/'+str(game.id), {
            'game_id': game.id,
            'stage': game.stage,
            'result': game.result,
            'timing': None,  # TODO: timing
            'node': game.board.current_node.to_dict() if game.board.current_node else {},
        })

    @BaseService.authenticated
    @BaseService.register
    def toggle_marked_dead(self, game_id, coord):
        with self._game_for_update(game_id) as game:
            if self.user not in [game.black_user, game.white_user]:
                raise InvalidPlayerError()

            if game.stage != 'counting':
                raise InvalidStageError()

            game.board.toggle_marked_dead(coord)
            self._update_score(game)
            game.apply_board_change()

            self.db.commit()
            self._publish_game_update(game)

    @BaseService.authenticated
    @BaseService.register
    def confirm_score(self, game_id, result):
        with self._game_for_update(game_id) as game:
            if self.user not in [game.black_user, game.white_user]:
                raise InvalidPlayerError()

            if game.stage != 'counting':
                raise InvalidStageError()

            if result != game.result:
                raise ServiceError('got incorrect result: {}'.format(result))

            if self.user == game.black_user:
                game.result_black_confirmed = game.result
            else:
                game.result_white_confirmed = game.result

            if game.result_black_confirmed == game.result_white_confirmed:
                game.stage = 'finished'
                self._finish_game(game)

    def _finish_game(self, game):
        if game.is_demo or game.stage != 'finished':
            return

        if game.is_ranked:
            RatingService(self.db).update_ratings(game)
            UserService(self.db, self.socket, game.black_user).publish_rating_update()
            UserService(self.db, self.socket, game.white_user).publish_rating_update()

        self.socket.publish('game_finished', game.to_frontend())
        self._publish_game_data(game)

        UserService(self.db, self.socket, game.black_user).publish_status()
        UserService(self.db, self.socket, game.white_user).publish_status()

    def _publish_game_data(self, game):
        self.socket.publish('game_data/'+str(game.id), game.to_frontend(full=True))

    @BaseService.authenticated
    @BaseService.register
    def set_current_node(self, game_id, node_id):
        game = self.db.query(Game).get(game_id)

        if not game.demo_control == self.user:
            raise InvalidPlayerError()

        if node_id >= len(game.board.tree):
            raise ServiceError('invalid node_id')

        game.board.current_node_id = node_id
        game.apply_board_change()
        self._publish_game_update(game)
