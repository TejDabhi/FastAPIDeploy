"""add content column to post tabel

Revision ID: fc952a10610e
Revises: f93cb643befd
Create Date: 2026-10-22 16:57:52.254889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc952a10610e'
down_revision: Union[str, Sequence[str], None] = 'f93cb643befd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post','content')
    pass
