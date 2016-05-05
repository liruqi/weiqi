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
from sqlalchemy import (Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, TypeDecorator, Text,
                        CheckConstraint)
from sqlalchemy.orm import validates, relationship, deferred
from sqlalchemy.orm.attributes import flag_modified
from weiqi.db import Base
from weiqi.glicko2 import player_from_dict, RatingEncoder
from weiqi.board import board_from_dict, BLACK, WHITE


class RatingData(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value, cls=RatingEncoder)

    def process_result_value(self, value, dialect):
        data = json.loads(value)
        return player_from_dict(data)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    display = Column(String, nullable=False)

    rating = Column(Float, nullable=False, default=0)
    rating_data = deferred(Column(RatingData, nullable=False))

    is_online = Column(Boolean, nullable=False, default=False)

    rooms = relationship('RoomUser', back_populates='user')
    messages = relationship('RoomMessage', back_populates='user')
    connections = relationship('Connection', back_populates='user')
    automatch = relationship('Automatch', back_populates='user')

    def set_password(self, pw):
        self.password = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, pw):
        return bcrypt.hashpw(pw.encode(), self.password.encode()) == self.password.encode()

    @validates('email')
    def validate_email(self, key, val):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', val):
            raise ValueError('invalid email address')
        return val

    @validates('display')
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

    def open_games(self, db):
        return db.query(Game).join(Room).join(RoomUser).filter(
            ((Game.is_demo.isnot(True)) & (Game.stage != 'finished') &
             ((Game.black_user == self) | (Game.white_user == self))) |
            (RoomUser.user == self))

    def apply_rating_data_change(self):
        """Notifies sqlalchemy about a change in the `rating_data` field.

        Needs to be called after in-place changes to the field.
        """
        flag_modified(self, 'rating_data')


class Connection(Base):
    __tablename__ = 'connections'

    id = Column(String, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='connections')

    ip = Column(String)


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = Column(String, nullable=False, default='')
    type = Column(Enum('main', 'direct', 'game', name='room_type'), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)

    users = relationship('RoomUser', back_populates='room')
    messages = relationship('RoomMessage', back_populates='room')
    games = relationship('Game', back_populates='room')

    def to_frontend(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
        }

    @staticmethod
    def open_rooms(db, user):
        if not user:
            return db.query(Room).filter_by(type='main')
        return db.query(Room).join('users').filter_by(user_id=user.id)


class RoomUser(Base):
    __tablename__ = 'room_users'

    room_id = Column(ForeignKey('rooms.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), primary_key=True)

    room = relationship('Room', back_populates='users')
    user = relationship('User', back_populates='rooms', lazy='joined')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    has_unread = Column(Boolean, nullable=False, default=False)

    def to_frontend(self):
        return {
            'room_id': self.room_id,
            'user_id': self.user_id,
            'user_display': self.user.display,
            'user_rating': self.user.rating,
        }


class RoomMessage(Base):
    __tablename__ = 'room_messages'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    room_id = Column(ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', back_populates='messages')

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='messages')

    user_display = Column(String, nullable=False)
    user_rating = Column(Float, nullable=False)

    message = Column(String, nullable=False)

    @validates('message')
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


class Automatch(Base):
    __tablename__ = 'automatch'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='automatch')

    user_rating = Column(Float, nullable=False)

    preset = Column(String, nullable=False)
    min_rating = Column(Float, nullable=False)
    max_rating = Column(Float, nullable=False)

    __table_args__ = (CheckConstraint('min_rating <= max_rating', name='rating_check'),)


class BoardData(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value.to_dict())

    def process_result_value(self, value, dialect):
        return board_from_dict(json.loads(value))


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room_id = Column(ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', back_populates='games')

    is_demo = Column(Boolean, nullable=False, default=False)
    is_ranked = Column(Boolean, nullable=False, default=True)

    stage = Column(Enum('playing', 'counting', 'finished', name='game_stage'), nullable=False)
    title = Column(String, nullable=False, default='')

    board = deferred(Column(BoardData, nullable=False))
    komi = Column(Float, nullable=False)

    result = Column(String, nullable=False, default='')
    result_black_confirmed = Column(String, nullable=False, default='')
    result_white_confirmed = Column(String, nullable=False, default='')

    black_user_id = Column(ForeignKey('users.id'), nullable=True)
    black_user = relationship('User', foreign_keys=[black_user_id])
    black_display = Column(String, nullable=False, default='')
    black_rating = Column(Float, nullable=True)

    white_user_id = Column(ForeignKey('users.id'), nullable=True)
    white_user = relationship('User', foreign_keys=[white_user_id])
    white_display = Column(String, nullable=False, default='')
    white_rating = Column(Float, nullable=True)

    demo_owner_id = Column(ForeignKey('users.id'), nullable=True)
    demo_owner = relationship('User', foreign_keys=[demo_owner_id])
    demo_owner_display = Column(String, nullable=False, default='')
    demo_owner_rating = Column(Float, nullable=True)

    demo_control_id = Column(ForeignKey('users.id'), nullable=True)
    demo_control = relationship('User', foreign_keys=[demo_control_id])
    demo_control_display = Column(String, nullable=False, default='')

    __table_args__ = (
        CheckConstraint('NOT is_ranked OR NOT is_demo'),
        CheckConstraint('is_demo OR black_user_id IS NOT NULL'),
        CheckConstraint('is_demo OR white_user_id IS NOT NULL'),
        CheckConstraint('NOT is_demo OR demo_owner_id IS NOT NULL'),
    )

    @property
    def current_user(self):
        if self.is_demo:
            return self.demo_owner
        return self.black_user if self.board.current == BLACK else self.white_user

    @property
    def winner_loser(self):
        if self.result.lower().startswith('b+'):
            return self.black_user, self.white_user
        elif self.result.lower().startswith('w+'):
            return self.white_user, self.black_user
        else:
            raise ValueError('could not determine winner and loser from game result: {}'.format(self.result))

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

        Needs to be called after in-place changes to the field.
        """
        flag_modified(self, 'board')


def datetime_to_frontend(date):
    return date.isoformat()
