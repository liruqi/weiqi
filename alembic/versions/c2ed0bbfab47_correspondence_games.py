"""correspondence games

Revision ID: c2ed0bbfab47
Revises: c10c022f7ac6
Create Date: 2016-06-09 18:28:24.235280

"""

# revision identifiers, used by Alembic.
revision = 'c2ed0bbfab47'
down_revision = 'c10c022f7ac6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('games', sa.Column('is_correspondence', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('timings', sa.Column('capped', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('challenges', sa.Column('is_correspondence', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('challenges', 'is_correspondence')
    op.drop_column('timings', 'capped')
    op.drop_column('games', 'is_correspondence')
