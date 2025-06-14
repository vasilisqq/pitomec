"""change_primary_ke

Revision ID: 82c4e23d187b
Revises: 9833a06d198f
Create Date: 2025-06-14 12:04:48.466232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82c4e23d187b'
down_revision: Union[str, None] = '9833a06d198f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
