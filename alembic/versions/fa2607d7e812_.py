"""empty message

Revision ID: fa2607d7e812
Revises: e10ad6e6f402
Create Date: 2025-06-09 20:37:35.329598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa2607d7e812'
down_revision: Union[str, None] = 'e10ad6e6f402'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
