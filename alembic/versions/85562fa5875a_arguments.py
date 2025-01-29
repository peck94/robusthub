"""arguments

Revision ID: 85562fa5875a
Revises: 6f6137c73827
Create Date: 2025-01-29 21:59:58.567447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85562fa5875a'
down_revision: Union[str, None] = '6f6137c73827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('attacks', 'arguments')
    op.drop_column('defenses', 'arguments')
    op.drop_column('models', 'arguments')

    op.add_column('benchmarks', sa.Column('attack_args', sa.String(), nullable=True, default='{{}}'))
    op.add_column('benchmarks', sa.Column('defense_args', sa.String(), nullable=True, default='{{}}'))
    op.add_column('benchmarks', sa.Column('model_args', sa.String(), nullable=True, default='{{}}'))


def downgrade() -> None:
    op.add_column('attacks', sa.Column('arguments', sa.String(), nullable=False, default='{}'))
    op.add_column('defenses', sa.Column('arguments', sa.String(), nullable=False, default='{}'))
    op.add_column('models', sa.Column('arguments', sa.String(), nullable=False, default='{}'))
