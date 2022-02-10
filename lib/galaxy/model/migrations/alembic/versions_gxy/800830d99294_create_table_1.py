"""create table 1

Revision ID: 800830d99294
Revises: 40aaada107df
Create Date: 2022-02-10 16:55:51.351091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '800830d99294'
down_revision = '40aaada107df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("a_gxy_1", sa.Column("id", sa.Integer, primary_key=True))


def downgrade():
    op.drop_table("a_gxy_1")
