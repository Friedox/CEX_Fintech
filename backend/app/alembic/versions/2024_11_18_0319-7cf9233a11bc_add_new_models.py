"""Add new models

Revision ID: 7cf9233a11bc
Revises: 6229230de8b1
Create Date: 2024-11-18 03:19:36.655512

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7cf9233a11bc"
down_revision: Union[str, None] = "6229230de8b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "orders", sa.Column("token_pair", sa.String(length=50), nullable=False)
    )
    op.add_column("orders", sa.Column("quantity", sa.Float(), nullable=False))
    op.add_column(
        "orders", sa.Column("is_filled", sa.Boolean(), nullable=True)
    )
    op.alter_column(
        "orders",
        "order_type",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum("buy", "sell", name="order_type"),
        existing_nullable=False,
    )
    op.alter_column(
        "orders",
        "price",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.drop_column("orders", "remaining_amount")
    op.drop_column("orders", "status")
    op.drop_column("orders", "amount")
    op.drop_column("orders", "pair")
    op.add_column(
        "trades", sa.Column("buyer_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "trades", sa.Column("seller_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "trades", sa.Column("token_pair", sa.String(length=50), nullable=False)
    )
    op.add_column("trades", sa.Column("quantity", sa.Float(), nullable=False))
    op.add_column(
        "trades",
        sa.Column(
            "timestamp",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "trades",
        "price",
        existing_type=sa.NUMERIC(precision=32, scale=8),
        type_=sa.Float(),
        existing_nullable=False,
    )
    op.create_index(op.f("ix_trades_id"), "trades", ["id"], unique=False)
    op.drop_constraint(
        "fk_trades_token_id_tokens", "trades", type_="foreignkey"
    )
    op.drop_constraint("fk_trades_user_id_users", "trades", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_trades_seller_id_users"),
        "trades",
        "users",
        ["seller_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_trades_buyer_id_users"),
        "trades",
        "users",
        ["buyer_id"],
        ["id"],
    )
    op.drop_column("trades", "created_at")
    op.drop_column("trades", "trade_type")
    op.drop_column("trades", "token_id")
    op.drop_column("trades", "user_id")
    op.drop_column("trades", "amount")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "trades",
        sa.Column(
            "amount",
            sa.NUMERIC(precision=32, scale=8),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "trades",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "trades",
        sa.Column(
            "token_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "trades",
        sa.Column(
            "trade_type",
            sa.VARCHAR(length=10),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "trades",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        op.f("fk_trades_buyer_id_users"), "trades", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_trades_seller_id_users"), "trades", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_trades_user_id_users", "trades", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_trades_token_id_tokens", "trades", "tokens", ["token_id"], ["id"]
    )
    op.drop_index(op.f("ix_trades_id"), table_name="trades")
    op.alter_column(
        "trades",
        "price",
        existing_type=sa.Float(),
        type_=sa.NUMERIC(precision=32, scale=8),
        existing_nullable=False,
    )
    op.drop_column("trades", "timestamp")
    op.drop_column("trades", "quantity")
    op.drop_column("trades", "token_pair")
    op.drop_column("trades", "seller_id")
    op.drop_column("trades", "buyer_id")
    op.add_column(
        "orders",
        sa.Column("pair", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "orders",
        sa.Column(
            "amount",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "status", sa.VARCHAR(length=20), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "remaining_amount",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.alter_column(
        "orders",
        "price",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "orders",
        "order_type",
        existing_type=sa.Enum("buy", "sell", name="order_type"),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
    )
    op.drop_column("orders", "is_filled")
    op.drop_column("orders", "quantity")
    op.drop_column("orders", "token_pair")
    # ### end Alembic commands ###