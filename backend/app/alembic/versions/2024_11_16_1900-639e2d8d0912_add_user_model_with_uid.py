"""Add User model with UID

Revision ID: 639e2d8d0912
Revises: a2e1d3ba73d0
Create Date: 2024-11-16 19:00:44.958422

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "639e2d8d0912"
down_revision: Union[str, None] = "a2e1d3ba73d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
