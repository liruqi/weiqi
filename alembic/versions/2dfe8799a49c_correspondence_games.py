"""correspondence games

Revision ID: 2dfe8799a49c
Revises: c10c022f7ac6
Create Date: 2016-06-08 18:01:55.453523

"""

# revision identifiers, used by Alembic.
revision = '2dfe8799a49c'
down_revision = 'c10c022f7ac6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('games', sa.Column('is_correspondence', sa.Boolean(), nullable=False, default=False, server_default='FALSE'))
    op.add_column('timings', sa.Column('cap', sa.Interval(), nullable=True))


def downgrade():
    op.drop_column('games', 'is_correspondence')
    op.drop_column('timings', 'cap')
