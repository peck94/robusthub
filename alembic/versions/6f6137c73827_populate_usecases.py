"""populate usecases

Revision ID: 6f6137c73827
Revises: 06dc1e8ce4a9
Create Date: 2025-01-24 15:40:24.847800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f6137c73827'
down_revision: Union[str, None] = '06dc1e8ce4a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

usecases = [
    {
        'title': 'Image classification',
        'short': 'Classification of images into discrete categories.',
        'full': 'image-classification.md',
        'thumb': '/assets/thumbnails/image-classification.png'
    },
    {
        'title': 'Medical image reconstruction',
        'short': 'Reconstruction of medical images, such as MR and CT, from noisy observations.',
        'full': 'medical-image-reconstruction.md',
        'thumb': '/assets/thumbnails/medical-image-reconstruction.png'
    },
    {
        'title': 'DGA detection',
        'short': 'Classification of internet domain names into malicious or benign.',
        'full': 'dga-detection.md',
        'thumb': '/assets/thumbnails/dga-detection.png'
    }
]

def upgrade() -> None:
    for uc in usecases:
        title = uc['title']
        short = uc['short']
        full = uc['full']
        thumb = uc['thumb']
        op.execute(f"insert into usecases (title, short_description, full_description, thumbnail) values ('{title}', '{short}', '{full}', '{thumb}')")


def downgrade() -> None:
    op.execute('delete from usecases')
    op.execute('delete from usecases_benchmarks')
