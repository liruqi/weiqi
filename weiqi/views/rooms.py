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
from weiqi.models import Room, RoomMessage, RoomUser, User

bp = Blueprint('rooms', __name__)


@bp.route('/<room_id>/message', methods=['POST'])
@login_required
def message(room_id):
    room = Room.query.get_or_404(room_id)
    msg = RoomMessage(
        room=room,
        user=current_user,
        user_display=current_user.display,
        user_rating=current_user.rating,
        message=request.form['message'])

    db.session.add(msg)
    db.session.commit()

    emit('room_message', msg.to_frontend(), room='room-'+str(room.id), namespace=None)

    return jsonify({})


@bp.route('/<room_id>/users')
def users(room_id):
    room = Room.query.get_or_404(room_id)
    query = RoomUser.query.filter_by(room_id=room.id).join('user').filter_by(is_online=True)

    return jsonify({'users': [ru.to_frontend() for ru in query]})
