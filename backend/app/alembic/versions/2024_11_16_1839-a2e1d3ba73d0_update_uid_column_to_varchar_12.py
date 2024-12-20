"""Update UID column to VARCHAR(12)

Revision ID: a2e1d3ba73d0
Revises: 7e5aad2456a0
Create Date: 2024-11-16 18:39:00.330723

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2e1d3ba73d0"
down_revision: Union[str, None] = "7e5aad2456a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "uid",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.String(length=16),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "uid",
        existing_type=sa.String(length=16),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
