"""more models

Revision ID: c74d88859ac3
Revises: d73c758c9b84
Create Date: 2025-01-30 10:13:01.285329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c74d88859ac3'
down_revision: Union[str, None] = 'd73c758c9b84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

models = [
    {'name': 'resnet50', 'title': 'ResNet-50', 'repo': 'pytorch/vision'},
    {'name': 'resnet101', 'title': 'ResNet-101', 'repo': 'pytorch/vision'},
    {'name': 'wide_resnet50_2', 'title': 'WideResNet-50', 'repo': 'pytorch/vision'},
]

def upgrade() -> None:
    for model in models:
        name = model['name']
        title = model['title']
        repo = model['repo']
        op.execute(f"insert into models (name, title, repo) values ('{name}', '{title}', '{repo}')")



def downgrade() -> None:
    for model in models:
        name = model['name']
        op.execute(f"delete from models where name = '{name}'")
