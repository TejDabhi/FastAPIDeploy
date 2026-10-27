
"""Auto Vote

Revision ID: 91f6e1351874
Revises: e313999bd18f
Create Date: 2026-10-23 11:37:57.236879
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision: str = '91f6e1351874'
down_revision: Union[str, Sequence[str], None] = 'e313999bd18f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Drop dependent table before its referenced user table
    op.drop_table('post')
    op.drop_table('user')

    # Add content as nullable first for existing rows
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=True)
    )

    # Give existing rows an empty string
    op.execute("UPDATE posts SET content = '' WHERE content IS NULL")

    # Make content mandatory
    op.alter_column(
        'posts',
        'content',
        existing_type=sa.String(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove the content column
    op.drop_column('posts', 'content')

    # Recreate user table first
    op.create_table(
        'user',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('password', sa.VARCHAR(), nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name='user_pkey'),
        sa.UniqueConstraint('email', name='user_email_key')
    )

    # Recreate post table and its foreign key
    op.create_table(
        'post',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('content', sa.VARCHAR(), nullable=False),
        sa.Column('owner_id', sa.INTEGER(), nullable=False),
        sa.Column(
            'published',
            sa.BOOLEAN(),
            server_default=sa.text('true'),
            nullable=False
        ),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ['owner_id'],
            ['user.id'],
            name='post_user_fk',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name='post_pkey')
    )
