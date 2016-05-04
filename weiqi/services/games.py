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
from tornado.web import HTTPError
from weiqi.services import BaseService
from weiqi.models import Game
from weiqi.board import RESIGN


class GameService(BaseService):
    __service_name__ = 'games'

    @BaseService.register
    def open(self, game_id):
        pass

    @BaseService.authenticated
    @BaseService.register
    def move(self, game_id, move):
        try:
            game = self.db.query(Game).options(undefer('board')).with_for_update().get(game_id)

            if game.is_demo:
                self._game_move_demo(game, move)
            else:
                self._game_move(game, move)

            self.db.commit()
        except:
            self.db.rollback()
            raise

        self._publish_game_update(game)

    def _game_move_demo(self, game, move):
        pass

    def _game_move(self, game, move):
        if self.user not in [game.black_user, game.white_user]:
            raise HTTPError(403)

        if game.stage == 'finished':
            raise HTTPError(403)

        # TODO: timing
        # if not game.timing.has_started:
        #   pass

        if move == RESIGN:
            pass

        if game.stage != 'playing':
            raise HTTPError(403)

        if game.current_user != self.user:
            raise HTTPError(403)

        # TODO: timing
        # if not game.timing.move_played(game.board.current):
        #   ... win by time ...

        game.board.play(move)
        game.apply_board_change()

        if game.board.both_passed:
            game.stage = 'counting'
            # TODO: update score

    def _publish_game_update(self, game):
        self.socket.publish('game_update/'+str(game.id), {
            'game_id': game.id,
            'stage': game.stage,
            'result': game.result,
            'timing': None,  # TODO: timing
            'node': game.board.current_node.to_dict(),
        })

    @BaseService.authenticated
    @BaseService.register
    def toggle_marked_dead(self, game_id, coord):
        pass
