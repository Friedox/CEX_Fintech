"""Add Order, Trade History models

Revision ID: bf8b147f0359
Revises: 71d1a34ee6ee
Create Date: 2024-11-18 00:06:54.670008

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bf8b147f0359"
down_revision: Union[str, None] = "71d1a34ee6ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_id", sa.Integer(), nullable=False),
        sa.Column("order_type", sa.String(length=10), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=32, scale=8), nullable=False),
        sa.Column("amount", sa.DECIMAL(precision=32, scale=8), nullable=False),
        sa.Column(
            "remaining_amount",
            sa.DECIMAL(precision=32, scale=8),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["token_id"], ["tokens.id"], name=op.f("fk_orders_token_id_tokens")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_orders_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)
    op.create_table(
        "trade_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token_id", sa.Integer(), nullable=False),
        sa.Column("buyer_id", sa.Integer(), nullable=True),
        sa.Column("seller_id", sa.Integer(), nullable=True),
        sa.Column("price", sa.DECIMAL(precision=32, scale=8), nullable=False),
        sa.Column("amount", sa.DECIMAL(precision=32, scale=8), nullable=False),
        sa.Column(
            "timestamp",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["buyer_id"],
            ["users.id"],
            name=op.f("fk_trade_history_buyer_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["users.id"],
            name=op.f("fk_trade_history_seller_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["token_id"],
            ["tokens.id"],
            name=op.f("fk_trade_history_token_id_tokens"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_trade_history")),
    )
    op.create_index(
        op.f("ix_trade_history_id"), "trade_history", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_trade_history_id"), table_name="trade_history")
    op.drop_table("trade_history")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")
    # ### end Alembic commands ###
