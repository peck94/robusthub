"""create attacks table

Revision ID: 932a0acf48c2
Revises: 7408911bf138
Create Date: 2024-12-31 15:11:49.251014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '932a0acf48c2'
down_revision: Union[str, None] = '7408911bf138'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('attacks',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(50), nullable=False),
                    sa.Column('title', sa.String(128), nullable=False),
                    sa.Column('repo', sa.String(128), nullable=False),
                    sa.Column('arguments', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_table('attacks')
