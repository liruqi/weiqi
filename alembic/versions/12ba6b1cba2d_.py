"""user avatar

Revision ID: 12ba6b1cba2d
Revises: b0be0cca1485
Create Date: 2016-05-06 15:38:18.966999

"""

# revision identifiers, used by Alembic.
revision = '12ba6b1cba2d'
down_revision = 'b0be0cca1485'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.Binary(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    ### end Alembic commands ###