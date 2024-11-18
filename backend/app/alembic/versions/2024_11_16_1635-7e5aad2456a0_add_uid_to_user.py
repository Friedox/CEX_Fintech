"""Add UID to User

Revision ID: 7e5aad2456a0
Revises: 5dde0fe599a7
Create Date: 2024-11-16 16:35:38.071607

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
import random
import string


# Helper function to generate random UID
def generate_uid(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# revision identifiers, used by Alembic.
revision: str = "7e5aad2456a0"
down_revision: Union[str, None] = "5dde0fe599a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the column as nullable first to avoid integrity issues
    op.add_column(
        "users", sa.Column("uid", sa.String(length=12), nullable=True)
    )

    # Populate the uid column with generated values
    users = table(
        "users",
        column("id", sa.Integer),  # Use the correct data type for `id`
        column("uid", sa.String(length=12)),
    )
    conn = op.get_bind()
    result = conn.execute(select(users.c.id))  # Select user IDs

    # Iterate through rows and update each with a unique UID
    for row in result.fetchall():
        conn.execute(
            users.update().where(result == row.id).values(uid=generate_uid())
        )

    # Alter the column to make it non-nullable
    op.alter_column("users", "uid", nullable=False)

    # Add a unique constraint to the column
    op.create_unique_constraint(op.f("uq_users_uid"), "users", ["uid"])


def downgrade() -> None:
    # Drop the unique constraint and column
    op.drop_constraint(op.f("uq_users_uid"), "users", type_="unique")
    op.drop_column("users", "uid")