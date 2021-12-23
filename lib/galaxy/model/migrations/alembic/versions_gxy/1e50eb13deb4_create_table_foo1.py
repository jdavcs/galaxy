"""create table foo1

Revision ID: 1e50eb13deb4
Revises: e7b6dcb09efd
Create Date: 2021-12-21 16:53:01.200726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e50eb13deb4'
down_revision = 'e7b6dcb09efd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foo1',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.String),
    )

def downgrade():
    op.drop_table('foo1')
