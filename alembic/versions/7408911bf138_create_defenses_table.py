"""create defenses table

Revision ID: 7408911bf138
Revises: 7603eb4fb584
Create Date: 2024-12-31 15:05:07.814966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7408911bf138'
down_revision: Union[str, None] = '7603eb4fb584'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('defenses',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(50), nullable=False),
                    sa.Column('title', sa.String(128), nullable=False),
                    sa.Column('repo', sa.String(128), nullable=False),
                    sa.Column('arguments', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_table('defenses')
