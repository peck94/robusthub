"""create benchmarks table

Revision ID: d4fc66c8dd8c
Revises: 932a0acf48c2
Create Date: 2024-12-31 15:12:50.468770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4fc66c8dd8c'
down_revision: Union[str, None] = '932a0acf48c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('benchmarks',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('model', sa.Integer, sa.ForeignKey('models.id'), nullable=False),
                    sa.Column('defense', sa.Integer, sa.ForeignKey('defenses.id'), nullable=False),
                    sa.Column('attack', sa.Integer, sa.ForeignKey('attacks.id'), nullable=False),
                    sa.Column('results', sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_table('benchmarks')