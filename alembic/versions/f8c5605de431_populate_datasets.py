"""populate datasets

Revision ID: f8c5605de431
Revises: d4ca2c28cf22
Create Date: 2025-01-07 23:57:16.817546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8c5605de431'
down_revision: Union[str, None] = 'd4ca2c28cf22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

datasets = [
    {'title': 'CIFAR-10', 'url': 'https://www.cs.toronto.edu/~kriz/cifar.html'},
    {'title': 'CIFAR-100', 'url': 'https://www.cs.toronto.edu/~kriz/cifar.html'},
    {'title': 'ImageNet', 'url': 'https://www.image-net.org/'},
    {'title': 'SVHN', 'url': 'http://ufldl.stanford.edu/housenumbers/'},
    {'title': 'MNIST', 'url': 'https://yann.lecun.com/exdb/mnist/'},
    {'title': 'Fashion-MNIST', 'url': 'https://github.com/zalandoresearch/fashion-mnist'}
]

def upgrade() -> None:
    for dataset in datasets:
        name = dataset['title']
        url = dataset['url']
        op.execute(f"insert into datasets (title, url) values ('{name}', '{url}')")

def downgrade() -> None:
    op.execute('delete from datasets')
