"""populate attacks

Revision ID: 4556382f93d1
Revises: 8d9005e5e5cc
Create Date: 2025-01-07 13:05:11.699358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4556382f93d1'
down_revision: Union[str, None] = '8d9005e5e5cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

attacks = [
    {'name': 'fgsm', 'title': 'Fast gradient sign', 'repo': 'peck94/robusthub', 'arguments': '{}'},
    {'name': 'pgd', 'title': 'Projected gradient descent', 'repo': 'peck94/robusthub', 'arguments': '{}'},
    {'name': 'apgd', 'title': 'Automatic projected gradient descent', 'repo': 'peck94/robusthub', 'arguments': '{}'},
    {'name': 'simba', 'title': 'Simple black-box attack', 'repo': 'peck94/robusthub', 'arguments': '{}'}
]

def upgrade() -> None:
    for attack in attacks:
        name = attack['name']
        title = attack['title']
        repo = attack['repo']
        args = attack['arguments']
        op.execute(f"insert into attacks (name, title, repo, arguments) values ('{name}', '{title}', '{repo}', '{args}')")


def downgrade() -> None:
    op.execute("delete from attacks")
