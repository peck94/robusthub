"""metrics

Revision ID: d73c758c9b84
Revises: 85562fa5875a
Create Date: 2025-01-29 22:32:51.654387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73c758c9b84'
down_revision: Union[str, None] = '85562fa5875a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('benchmarks', sa.Column('metrics', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('benchmarks', 'metrics')
