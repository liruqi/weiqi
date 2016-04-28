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

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import validates, relationship
from datetime import datetime
import re
import bcrypt
from weiqi.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    display = Column(String, nullable=False)
    rating = Column(Float, nullable=False, default=0)

    rooms = relationship('RoomUser', back_populates='user')
    messages = relationship('RoomMessage', back_populates='user')
    connections = relationship('Connection', back_populates='user')

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


class Connection(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='connections')

    ip = Column(String)


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = Column(String, nullable=False, default='Room')
    type = Column(Enum('main', 'direct', 'game', name='room_type'), nullable=False)

    users = relationship('RoomUser', back_populates='room')
    messages = relationship('RoomMessage', back_populates='room')

    def to_frontend(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
        }


class RoomUser(Base):
    __tablename__ = 'room_users'

    room_id = Column(ForeignKey('rooms.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), primary_key=True)

    room = relationship('Room', back_populates='users')
    user = relationship('User', back_populates='rooms', lazy='joined')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    has_unread = Column(Boolean, nullable=False, default=False)


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


def datetime_to_frontend(date):
    return date.isoformat()
