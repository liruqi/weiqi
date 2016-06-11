"""correspondence settings

Revision ID: 489ebff657cb
Revises: c2ed0bbfab47
Create Date: 2016-06-10 19:29:49.789079

"""

# revision identifiers, used by Alembic.
revision = '489ebff657cb'
down_revision = 'c2ed0bbfab47'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('correspondence_emails', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    op.drop_column('users', 'correspondence_emails')
