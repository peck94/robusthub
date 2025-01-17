"""create usecases

Revision ID: 06dc1e8ce4a9
Revises: f8c5605de431
Create Date: 2025-01-16 11:34:01.311975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06dc1e8ce4a9'
down_revision: Union[str, None] = 'f8c5605de431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('usecases',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('title', sa.String(128), nullable=False),
                    sa.Column('short_description', sa.String(256), nullable=False),
                    sa.Column('full_description', sa.String(256), nullable=False))
    op.create_table('usecases_benchmarks',
                    sa.Column('usecase_id', sa.Integer, sa.ForeignKey('usecases.id')),
                    sa.Column('benchmark_id', sa.Integer, sa.ForeignKey('benchmarks.id')))


def downgrade() -> None:
    op.drop_table('usecases')
    op.drop_table('usecases_benchmarks')
