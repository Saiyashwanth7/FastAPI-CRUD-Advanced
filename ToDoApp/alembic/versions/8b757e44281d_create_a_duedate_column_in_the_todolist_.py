"""Create a duedate column in the todolist db

Revision ID: 8b757e44281d
Revises: 80c655e9cb5a
Create Date: 2025-08-02 09:20:54.398249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b757e44281d'
down_revision: Union[str, Sequence[str], None] = '80c655e9cb5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("todolist",sa.Column("DueDate",sa.DATE(),nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
