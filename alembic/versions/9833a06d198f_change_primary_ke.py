"""change_primary_ke

Revision ID: 9833a06d198f
Revises: e9afdacde60a
Create Date: 2025-06-11 16:14:28.454251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9833a06d198f'
down_revision: Union[str, None] = 'e9afdacde60a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_primary_key(
        'pets_pkey',          # Имя нового PK
        'pet',               # Имя таблицы
        ['owner1', 'owner2']  # Колонки для PK
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
