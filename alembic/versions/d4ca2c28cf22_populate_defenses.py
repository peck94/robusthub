"""populate defenses

Revision ID: d4ca2c28cf22
Revises: 4556382f93d1
Create Date: 2025-01-07 13:17:14.636495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4ca2c28cf22'
down_revision: Union[str, None] = '4556382f93d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

defenses = [
    {'name': 'adversarial_training', 'title': 'Adversarial training', 'repo': 'peck94/robusthub', 'arguments': '{}'},
    {'name': 'randomized_smoothing', 'title': 'Randomized smoothing', 'repo': 'peck94/robusthub', 'arguments': '{}'},
    {'name': 'vanilla_defense', 'title': 'Vanilla', 'repo': 'peck94/robusthub', 'arguments': '{}'}
]

def upgrade() -> None:
    for defense in defenses:
        name = defense['name']
        title = defense['title']
        repo = defense['repo']
        args = defense['arguments']
        op.execute(f"insert into defenses (name, title, repo, arguments) values ('{name}', '{title}', '{repo}', '{args}')")


def downgrade() -> None:
    op.execute("delete from defenses")
