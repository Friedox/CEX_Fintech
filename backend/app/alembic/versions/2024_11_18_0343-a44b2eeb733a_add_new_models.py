"""Add new models

Revision ID: a44b2eeb733a
Revises: e1b26c62bf2a
Create Date: 2024-11-18 03:43:19.702750

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a44b2eeb733a"
down_revision: Union[str, None] = "e1b26c62bf2a"
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
