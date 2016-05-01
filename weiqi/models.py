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
import re
import bcrypt
import json
from flask_login import UserMixin
from sqlalchemy.orm.attributes import flag_modified
from weiqi import db
from weiqi.glicko2 import player_from_dict, RatingEncoder
from weiqi.board import board_from_dict, BLACK, WHITE


class RatingData(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value, cls=RatingEncoder)

    def process_result_value(self, value, dialect):
        data = json.loads(value)
        return player_from_dict(data)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    display = db.Column(db.String, nullable=False)

    rating = db.Column(db.Float, nullable=False, default=0)
    rating_data = db.deferred(db.Column(RatingData, nullable=False))

    is_online = db.Column(db.Boolean, nullable=False, default=False)

    rooms = db.relationship('RoomUser', back_populates='user')
    messages = db.relationship('RoomMessage', back_populates='user')
    connections = db.relationship('Connection', back_populates='user')
    automatch = db.relationship('Automatch', back_populates='user')

    def set_password(self, pw):
        self.password = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, pw):
        return bcrypt.hashpw(pw.encode(), self.password.encode()) == self.password.encode()

    @db.validates('email')
    def validate_email(self, key, val):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', val):
            raise ValueError('invalid email address')
        return val

    @db.validates('display')
    def validate_display(self, key, val):
        if not re.match(r'^[a-zA-Z0-9_-]{2,12}$', val):
            raise ValueError('invalid display name')
        return val

    def to_frontend(self):
        return {
            'id': self.id,
            'display': self.display,
            'rating': self.rating,
        }


class Connection(db.Model):
    __tablename__ = 'connections'

    id = db.Column(db.String, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', back_populates='connections')

    ip = db.Column(db.String)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String, nullable=False, default='')
    type = db.Column(db.Enum('main', 'direct', 'game', name='room_type'), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)

    users = db.relationship('RoomUser', back_populates='room')
    messages = db.relationship('RoomMessage', back_populates='room')
    games = db.relationship('Game', back_populates='room')

    def to_frontend(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
        }

    @classmethod
    def open_rooms(cls, user):
        if not user or not user.is_authenticated:
            return cls.query.filter_by(type='main')
        return cls.query.join('users').filter_by(user_id=user.id)


class RoomUser(db.Model):
    __tablename__ = 'room_users'

    room_id = db.Column(db.ForeignKey('rooms.id'), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)

    room = db.relationship('Room', back_populates='users')
    user = db.relationship('User', back_populates='rooms', lazy='joined')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    has_unread = db.Column(db.Boolean, nullable=False, default=False)

    def to_frontend(self):
        return {
            'room_id': self.room_id,
            'user_id': self.user_id,
            'user_display': self.user.display,
            'user_rating': self.user.rating,
        }


class RoomMessage(db.Model):
    __tablename__ = 'room_messages'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    room_id = db.Column(db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', back_populates='messages')

    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='messages')

    user_display = db.Column(db.String, nullable=False)
    user_rating = db.Column(db.Float, nullable=False)

    message = db.Column(db.String, nullable=False)

    @db.validates('message')
    def validate_message(self, key, val):
        if not val or not val.strip():
            raise ValueError('message cannot be empty')
        return val.strip()

    def to_frontend(self):
        return {
            'id': self.id,
            'created_at': datetime_to_frontend(self.created_at),
            'room_id': self.room_id,
            'user_id': self.user_id,
            'user_display': self.user_display,
            'user_rating': self.user_rating,
            'message': self.message
        }


class Automatch(db.Model):
    __tablename__ = 'automatch'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='automatch')

    user_rating = db.Column(db.Float, nullable=False)

    preset = db.Column(db.String, nullable=False)
    min_rating = db.Column(db.Float, nullable=False)
    max_rating = db.Column(db.Float, nullable=False)

    __table_args__ = (db.CheckConstraint('min_rating <= max_rating', name='rating_check'),)


class BoardData(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value.to_dict())

    def process_result_value(self, value, dialect):
        return board_from_dict(json.loads(value))


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room_id = db.Column(db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', back_populates='games')

    is_demo = db.Column(db.Boolean, nullable=False, default=False)
    is_ranked = db.Column(db.Boolean, nullable=False, default=True)

    stage = db.Column(db.Enum('playing', 'counting', 'finished', name='game_stage'), nullable=False)
    title = db.Column(db.String, nullable=False, default='')

    board = db.deferred(db.Column(BoardData, nullable=False))
    komi = db.Column(db.Float, nullable=False)

    result = db.Column(db.String, nullable=False, default='')
    result_black_confirmed = db.Column(db.String, nullable=False, default='')
    result_white_confirmed = db.Column(db.String, nullable=False, default='')

    black_user_id = db.Column(db.ForeignKey('users.id'), nullable=True)
    black_user = db.relationship('User', foreign_keys=[black_user_id])
    black_display = db.Column(db.String, nullable=False, default='')
    black_rating = db.Column(db.Float, nullable=True)

    white_user_id = db.Column(db.ForeignKey('users.id'), nullable=True)
    white_user = db.relationship('User', foreign_keys=[white_user_id])
    white_display = db.Column(db.String, nullable=False, default='')
    white_rating = db.Column(db.Float, nullable=True)

    demo_owner_id = db.Column(db.ForeignKey('users.id'), nullable=True)
    demo_owner = db.relationship('User', foreign_keys=[demo_owner_id])
    demo_owner_display = db.Column(db.String, nullable=False, default='')
    demo_owner_rating = db.Column(db.Float, nullable=True)

    demo_control_id = db.Column(db.ForeignKey('users.id'), nullable=True)
    demo_control = db.relationship('User', foreign_keys=[demo_control_id])
    demo_control_display = db.Column(db.String, nullable=False, default='')

    __table_args__ = (
        db.CheckConstraint('NOT is_ranked OR NOT is_demo'),
        db.CheckConstraint('is_demo OR black_user_id IS NOT NULL'),
        db.CheckConstraint('is_demo OR white_user_id IS NOT NULL'),
        db.CheckConstraint('NOT is_demo OR demo_owner_id IS NOT NULL'),
    )

    @property
    def current_user(self):
        if self.is_demo:
            return self.demo_owner
        return self.black_user if self.board.current == BLACK else self.white_user

    def to_frontend(self, full=False):
        """Returns a dictionary with the game information.
        Will not return board data unless `full` is set to True.
        """
        data = {
            'id': self.id,
            'created_at': datetime_to_frontend(self.created_at),
            'room_id': self.room_id,
            'is_demo': self.is_demo,
            'is_ranked': self.is_ranked,
            'stage': self.stage,
            'title': self.title,
            'komi': self.komi,
            'result': self.result,
            'black_user_id': self.black_user_id,
            'black_display': self.black_display,
            'black_rating': self.black_rating,
            'white_user_id': self.white_user_id,
            'white_display': self.white_display,
            'white_rating': self.white_rating,
            'demo_owner_id': self.demo_owner_id,
            'demo_owner_display': self.demo_owner_display,
            'demo_owner_rating': self.demo_owner_rating,
        }

        if full:
            data.update({
                'board': self.board.to_dict(),
                'result_black_confirmed': self.result_black_confirmed,
                'result_white_confirmed': self.result_white_confirmed,
                'demo_control_id': self.demo_control_id,
                'demo_control_display': self.demo_control_display,
            })

        return data

    def apply_board_change(self):
        """Notifies sqlalchemy about a change in the `board` field.

        This is required because sqlalchemy detects only changes for field values, but `board`
        is usually changed in-place.
        """
        flag_modified(self, 'board')


def datetime_to_frontend(date):
    return date.isoformat()
