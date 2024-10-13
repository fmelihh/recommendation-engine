"""comments table

Revision ID: de3b0f448b4c
Revises: 58fd94ccc2c2
Create Date: 2024-10-13 20:59:59.703165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de3b0f448b4c'
down_revision: Union[str, None] = '58fd94ccc2c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
