"""Add is_webapp column to worker_process

Revision ID: 017839a93603
Revises: 1d1d7bf6ac02
Create Date: 2025-12-09 18:21:40.534186

"""

from sqlalchemy import (
    Column,
    Boolean,
)

from galaxy.model.migrations.util import (
    add_column,
    drop_column,
)

# revision identifiers, used by Alembic.
revision = '017839a93603'
down_revision = '1d1d7bf6ac02'
branch_labels = None
depends_on = None

table_name = "worker_process"
column_name = "is_webapp"


def upgrade():
    add_column(table_name, Column(column_name, Boolean))


def downgrade():
    drop_column(table_name, column_name)
