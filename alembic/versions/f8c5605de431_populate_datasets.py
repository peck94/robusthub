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
    {'name': 'CIFAR-10', 'url': 'https://www.cs.toronto.edu/~kriz/cifar.html'},
    {'name': 'CIFAR-100', 'url': 'https://www.cs.toronto.edu/~kriz/cifar.html'},
    {'name': 'ImageNet', 'url': 'https://www.image-net.org/'},
    {'name': 'SVHN', 'url': 'http://ufldl.stanford.edu/housenumbers/'},
    {'name': 'MNIST', 'url': 'https://yann.lecun.com/exdb/mnist/'},
    {'name': 'Fashion-MNIST', 'url': 'https://github.com/zalandoresearch/fashion-mnist'}
]

def upgrade() -> None:
    for dataset in datasets:
        name = dataset['name']
        url = dataset['url']
        op.execute(f"insert into datasets (name, url) values ('{name}', '{url}')")

def downgrade() -> None:
    op.execute('delete from datasets')
