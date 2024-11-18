"""Add missing tables

Revision ID: 648db296d2db
Revises: 79c8ecad7d2f
Create Date: 2024-11-16 23:58:04.025087

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "648db296d2db"
down_revision: Union[str, None] = "79c8ecad7d2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tokens",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("total_supply", sa.DECIMAL(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tokens")),
        sa.UniqueConstraint("name", name=op.f("uq_tokens_name")),
        sa.UniqueConstraint("ticker", name=op.f("uq_tokens_ticker")),
    )
    op.create_table(
        "user_assets",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token_id", sa.UUID(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=8), nullable=False),
        sa.ForeignKeyConstraint(
            ["token_id"],
            ["tokens.id"],
            name=op.f("fk_user_assets_token_id_tokens"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_assets_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_assets")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_assets")
    op.drop_table("tokens")
    # ### end Alembic commands ###
