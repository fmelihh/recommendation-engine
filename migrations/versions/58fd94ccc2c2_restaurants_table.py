"""restaurants table

Revision ID: 58fd94ccc2c2
Revises: de011ed478ca
Create Date: 2024-10-13 20:59:52.879170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58fd94ccc2c2'
down_revision: Union[str, None] = 'de011ed478ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
