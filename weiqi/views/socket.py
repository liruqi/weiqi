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

from flask import request
from flask_socketio import emit, join_room
from flask_login import current_user
from weiqi import socketio, db
from weiqi.models import Connection, Room, Game, RoomUser


@socketio.on('connect')
def connect():
    emit('connection_data', _connection_data())
    _join_open_rooms_and_games()
    _insert_connection()
    _update_status()


@socketio.on('disconnect')
def disconnect():
    _delete_connection()
    _update_status()


@socketio.on('open_game')
def open_game(game_id):
    game = Game.query.get(game_id)
    join_room('game/'+str(game_id))
    _join_room_user(game.room_id)
    emit('game_data', game.to_frontend(full=True))


def _connection_data():
    data = {}

    if current_user.is_authenticated:
        data.update({
            'user_id': current_user.id,
            'user_display': current_user.display,
            'rating': current_user.rating,
        })

    data.update(_connection_data_rooms())
    data.update(_connection_data_games())

    return data


def _connection_data_rooms():
    rooms = []
    logs = {}

    for room in Room.open_rooms(current_user):
        rooms.append(room.to_frontend())
        logs[room.id] = [m.to_frontend() for m in room.messages]

    return {'rooms': rooms, 'room_logs': logs}


def _connection_data_games():
    if not current_user.is_authenticated:
        return {}

    return {
        'open_games': [g.to_frontend(full=True) for g in current_user.open_games]
    }


def _join_open_rooms_and_games():
    for room in Room.open_rooms(current_user):
        join_room('room/'+str(room.id))

        if room.type == 'game':
            join_room('game/'+str(room.games[0].id))


def _join_room_user(room_id):
    join_room('room/'+str(room_id))

    if current_user.is_authenticated:
        if RoomUser.query.filter_by(room_id=room_id, user=current_user).count() == 0:
            db.session.add(RoomUser(room_id=room_id, user=current_user))
            db.session.commit()


def _insert_connection():
    conn = Connection(id=request.sid,
                      user=current_user if current_user.is_authenticated else None,
                      ip=request.remote_addr)

    db.session.add(conn)
    db.session.commit()


def _delete_connection():
    Connection.query.filter_by(id=request.sid).delete()
    db.session.commit()


def _update_status():
    if not current_user.is_authenticated:
        return

    current_user.is_online = Connection.query.filter_by(user_id=current_user.id).count() > 0
    db.session.commit()

    for ru in current_user.rooms:
        if current_user.is_online:
            emit('room_user', ru.to_frontend(), room='room/'+str(ru.room_id))
        else:
            emit('room_user_left', ru.to_frontend(), room='room/'+str(ru.room_id))
