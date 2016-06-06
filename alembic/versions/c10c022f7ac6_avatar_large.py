"""avatar_large

Revision ID: c10c022f7ac6
Revises: 028d3ac7278e
Create Date: 2016-06-06 19:00:11.491007

"""

# revision identifiers, used by Alembic.
revision = 'c10c022f7ac6'
down_revision = '028d3ac7278e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image
from io import BytesIO

Session = sessionmaker()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    avatar = sa.Column(sa.Binary(), nullable=True)
    avatar_large = sa.Column(sa.Binary(), nullable=True)


def upgrade():
    op.add_column('users', sa.Column('avatar_large', sa.Binary(), nullable=True))

    bind = op.get_bind()
    session = Session(bind=bind)

    for user in session.query(User):
        if not user.avatar:
            continue

        user.avatar_large = user.avatar

        img = Image.open(BytesIO(user.avatar_large))
        img.thumbnail((64, 64))

        data = BytesIO()
        img.save(data, format='JPEG', quality=90, optimize=True, progressive=True)

        user.avatar = data.getvalue()

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    for user in session.query(User):
        user.avatar = user.avatar_large

    session.commit()

    op.drop_column('users', 'avatar_large')
