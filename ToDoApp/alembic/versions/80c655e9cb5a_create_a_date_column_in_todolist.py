"""Create a date column in todolist

Revision ID: 80c655e9cb5a
Revises: 
Create Date: 2025-08-02 08:58:35.760315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80c655e9cb5a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("todolist",sa.Column("create_at",sa.TIMESTAMP(timezone=True),nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    pass
