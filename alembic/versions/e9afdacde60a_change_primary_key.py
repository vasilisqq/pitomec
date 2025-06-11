"""change_primary_key

Revision ID: e9afdacde60a
Revises: 69e45c8d9f5b
Create Date: 2025-06-11 16:04:44.135402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9afdacde60a'
down_revision: Union[str, None] = '69e45c8d9f5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
