"""create tablefoo

Revision ID: 3a45b497fe25
Revises: 7cad1c686b6b
Create Date: 2021-12-08 15:07:26.993362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a45b497fe25'
down_revision = '7cad1c686b6b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )


def downgrade():
    os.drop_table('foo')
