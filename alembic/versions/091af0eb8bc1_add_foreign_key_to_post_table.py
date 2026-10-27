"""Add Foreign key to post table

Revision ID: 091af0eb8bc1
Revises: 324fa080e801
Create Date: 2026-10-23 10:35:53.029058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '091af0eb8bc1'
down_revision: Union[str, Sequence[str], None] = '324fa080e801'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',
                          source_table='post',
                          referent_table='user',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='post')
    op.drop_column('post','owner_id')
    pass
