"""create table foo3

Revision ID: ac8cc0793194
Revises: 4ec69e681ca3
Create Date: 2021-12-08 15:10:57.509171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac8cc0793194'
down_revision = '4ec69e681ca3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo3',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )


def downgrade():
    os.drop_table('foo3')
