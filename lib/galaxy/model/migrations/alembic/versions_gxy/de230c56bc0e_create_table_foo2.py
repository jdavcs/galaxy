"""create table foo2

Revision ID: de230c56bc0e
Revises: 1e50eb13deb4
Create Date: 2021-12-21 16:53:05.231216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de230c56bc0e'
down_revision = '1e50eb13deb4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo2',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )


def downgrade():
    op.drop_table('foo2')
