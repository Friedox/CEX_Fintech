"""Add missing tables

Revision ID: c6230f9ea1f8
Revises: c3e27f69b9b6
Create Date: 2024-11-17 20:38:24.441620
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c6230f9ea1f8"
down_revision = "c3e27f69b9b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alter 'id' column to Integer
    op.alter_column(
        "users",
        "id",
        existing_type=postgresql.UUID(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="id::integer",
    )
    # Add index for 'id' column
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    # Drop the index
    op.drop_index(op.f("ix_users_id"), table_name="users")
    # Revert 'id' column back to UUID
    op.alter_column(
        "users",
        "id",
        existing_type=sa.Integer(),
        type_=postgresql.UUID(),
        existing_nullable=False,
        postgresql_using="id::uuid",
    )
