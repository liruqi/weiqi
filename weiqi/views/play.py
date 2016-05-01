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

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from weiqi import db
from weiqi.board import Board
from weiqi.models import Automatch, Game, Room, RoomUser
from weiqi.rating import rating_range

bp = Blueprint('play', __name__)


@bp.route('/automatch', methods=['POST'])
@login_required
def automatch():
    preset = request.form['preset']
    max_hc = int(request.form['max_hc'])

    start, end = rating_range(current_user.rating, max_hc)
    game = None

    try:
        query = Automatch.query.with_for_update()
        query = query.filter(Automatch.min_rating <= current_user.rating,
                             Automatch.max_rating >= current_user.rating,
                             Automatch.user_rating >= start,
                             Automatch.user_rating <= end)
        query = query.order_by(Automatch.created_at)
        other = query.first()

        if other:
            game = _create_game(current_user, other.user, preset, True)
            db.session.delete(other)
        else:
            item = Automatch(preset=preset,
                             user=current_user,
                             user_rating=current_user.rating,
                             min_rating=start,
                             max_rating=end)
            db.session.add(item)

        db.session.commit()
    except:
        db.session.rollback()
        raise

    if game:
        _emit_game_started(game)

    return jsonify({})


def _create_game(user, other, preset, ranked):
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

    db.session.add(room)
    db.session.add(ru)
    db.session.add(ru2)
    db.session.add(game)

    return game


def _emit_game_started(game):
    emit('game_started', game.to_frontend(), broadcast=True, namespace=None)


@bp.route('/automatch/cancel', methods=['POST'])
@login_required
def cancel_automatch():
    pass


@bp.route('/upload-sgf', methods=['POST'])
@login_required
def upload_sgf():
    pass


@bp.route('/create-demo', methods=['POST'])
@login_required
def create_demo():
    pass


@bp.route('/challenge', methods=['POST'])
@login_required
def challenge():
    pass
