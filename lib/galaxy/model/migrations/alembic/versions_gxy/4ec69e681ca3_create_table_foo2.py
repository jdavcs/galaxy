"""create table foo2

Revision ID: 4ec69e681ca3
Revises: 3a45b497fe25
Create Date: 2021-12-08 15:10:54.894186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec69e681ca3'
down_revision = '3a45b497fe25'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo2',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )


def downgrade():
    pass
    os.drop_table('foo2')
