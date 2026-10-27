"""Create Posts Table

Revision ID: f93cb643befd
Revises: 
Create Date: 2026-10-22 16:02:53.756875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f93cb643befd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('post',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('post')
    pass
