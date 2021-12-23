"""create table foo3

Revision ID: 99043a68425c
Revises: de230c56bc0e
Create Date: 2021-12-21 16:53:07.226310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99043a68425c'
down_revision = 'de230c56bc0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo3',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )


def downgrade():
    op.drop_table('foo3')
