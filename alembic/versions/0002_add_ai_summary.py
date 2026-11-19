"""add ai summary

Revision ID: 0002_add_ai_summary
Revises: 0001_add_description
Create Date: 2026-09-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0002_add_ai_summary"
down_revision = "0001_add_description"
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "documents" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("documents")}
        if "ai_summary" not in columns:
            op.add_column("documents", sa.Column("ai_summary", sa.Text(), nullable=True))

def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if "documents" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("documents")}
        if "ai_summary" in columns:
            op.drop_column("documents", "ai_summary")
