"""populate models

Revision ID: 8d9005e5e5cc
Revises: d4fc66c8dd8c
Create Date: 2025-01-01 20:51:20.523421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d9005e5e5cc'
down_revision: Union[str, None] = 'd4fc66c8dd8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

models = [
    {'name': 'resnet18', 'repo': 'pytorch/vision', 'arguments': '{}'},
    {'name': 'wide_resnet101_2', 'repo': 'pytorch/vision', 'arguments': '{}'}
]

def upgrade() -> None:
    for model in models:
        name = model['name']
        repo = model['repo']
        args = model['arguments']
        op.execute(f"insert into models (name, repo, arguments) values ('{name}', '{repo}', '{args}')")


def downgrade() -> None:
    op.execute("delete from models")
