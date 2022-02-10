"""create table 2

Revision ID: e7e3ad6a4f41
Revises: 800830d99294
Create Date: 2022-02-10 16:55:56.040944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7e3ad6a4f41'
down_revision = '800830d99294'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("a_gxy_2", sa.Column("id", sa.Integer, primary_key=True))


def downgrade():
    op.drop_table("a_gxy_2")
