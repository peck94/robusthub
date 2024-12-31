"""create models table

Revision ID: 7603eb4fb584
Revises: 
Create Date: 2024-12-31 14:57:25.728154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7603eb4fb584'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('models',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(50), nullable=False),
                    sa.Column('repo', sa.String(128), nullable=False),
                    sa.Column('arguments', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_table('models')
