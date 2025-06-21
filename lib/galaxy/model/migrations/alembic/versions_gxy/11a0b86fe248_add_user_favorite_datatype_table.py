"""Add user_favorite_datatype table

Revision ID: 11a0b86fe248
Revises: c716ee82337b
Create Date: 2025-06-21 17:20:34.467048

"""

import sqlalchemy as sa

from galaxy.model.migrations.util import (
    create_table,
    drop_table,
)

# revision identifiers, used by Alembic.
revision = "11a0b86fe248"
down_revision = "c716ee82337b"
branch_labels = None
depends_on = None

TABLE_NAME = "user_favorite_datatype"


def upgrade():
    create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("galaxy_user.id")),
        sa.Column("datatype", sa.String(255)),
    )


def downgrade():
    drop_table(TABLE_NAME)
