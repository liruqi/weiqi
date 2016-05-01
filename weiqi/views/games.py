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

from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from flask_socketio import emit
from weiqi import db
from weiqi.models import Game
from weiqi.board import RESIGN

bp = Blueprint('games', __name__)


@bp.route('/<game_id>/move', methods=['POST'])
@login_required
def game_move(game_id):
    move = int(request.form['move'])

    try:
        game = Game.query.options(db.undefer('board')).with_for_update().get(game_id)

        if game.is_demo:
            _game_move_demo(game, move)
        else:
            _game_move(game, move)

        db.session.commit()
    except:
        db.session.rollback()
        raise

    return jsonify({})


def _game_move_demo(game, move):
    pass


def _game_move(game, move):
    if current_user not in [game.black_user, game.white_user]:
        abort(403)

    if game.stage == 'finished':
        abort(403)

    # TODO: timing
    # if not game.timing.has_started:
    #   pass

    if move == RESIGN:
        pass

    if game.stage != 'playing':
        abort(403)

    if game.current_user != current_user:
        abort(403)

    # TODO: timing
    # if not game.timing.move_played(game.board.current):
    #   ... win by time ...

    game.board.play(move)
    game.apply_board_change()

    if game.board.both_passed:
        game.stage = 'counting'
        # TODO: update score
