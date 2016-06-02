"""direct_rooms

Revision ID: 566ec65280e8
Revises: 187feb1b9af0
Create Date: 2016-05-25 18:14:02.957810

"""

# revision identifiers, used by Alembic.
revision = '566ec65280e8'
down_revision = '187feb1b9af0'
branch_labels = None
depends_on = None

from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql

Session = sessionmaker()
Base = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Enum('main', 'direct', 'game', name='room_type'), nullable=False)


class RoomUser(Base):
    __tablename__ = 'room_users'
    room_id = sa.Column(sa.ForeignKey('Room'), primary_key=True)
    user_id = sa.Column(sa.Integer, primary_key=True)


class DirectRoom(Base):
    __tablename__ = 'direct_rooms'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    room_id = sa.Column(sa.Integer, nullable=False)
    user_one_id = sa.Column(sa.Integer, nullable=False)
    user_two_id = sa.Column(sa.Integer, nullable=False)
    user_one_has_unread = sa.Column(sa.Boolean, nullable=False, default=False)
    user_two_has_unread = sa.Column(sa.Boolean, nullable=False, default=False)


def upgrade():
    op.create_table('direct_rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('room_id', sa.Integer(), nullable=False),
                    sa.Column('user_one_id', sa.Integer(), nullable=False),
                    sa.Column('user_two_id', sa.Integer(), nullable=False),
                    sa.Column('user_one_has_unread', sa.Boolean(), nullable=False, default=False),
                    sa.Column('user_two_has_unread', sa.Boolean(), nullable=False, default=False),
                    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
                    sa.ForeignKeyConstraint(['user_one_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['user_two_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    bind = op.get_bind()
    session = Session(bind=bind)

    for room in session.query(Room).filter_by(type='direct'):
        users = session.query(RoomUser).filter_by(room_id=room.id)
        one = users.first()
        two = users.filter(RoomUser.user_id != one.user_id).first()

        if not one or not two or one == two:
            continue

        direct = DirectRoom(room_id=room.id, user_one_id=one.user_id, user_two_id=two.user_id)
        session.add(direct)

    session.commit()

    with op.batch_alter_table('room_users') as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('has_unread')


def downgrade():
    op.drop_table('direct_rooms')
    op.add_column('room_users', sa.Column('has_unread', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('room_users', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
