"""add description

Revision ID: 0001_add_description
Revises:
Create Date: 2026-09-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0001_add_description"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    tables = inspector.get_table_names()

    if "documents" not in tables:
        op.create_table(
            "documents",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("title", sa.String(length=120), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("priority", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("description", sa.String(length=250), nullable=True),
        )
    else:
        columns = {column["name"] for column in inspector.get_columns("documents")}
        if "priority" not in columns:
            op.add_column("documents", sa.Column("priority", sa.Integer(), nullable=False, server_default="1"))
        if "description" not in columns:
            op.add_column("documents", sa.Column("description", sa.String(length=250), nullable=True))

def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "documents" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("documents")}
        if "description" in columns:
            op.drop_column("documents", "description")
