"""Add Token, UserAsset models

Revision ID: 79c8ecad7d2f
Revises: 20ed6dfa5f89
Create Date: 2024-11-16 23:15:29.258836

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79c8ecad7d2f"
down_revision: Union[str, None] = "20ed6dfa5f89"
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
