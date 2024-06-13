"""create a posts table

Revision ID: 3e61691ae851
Revises: 
Create Date: 2024-06-12 14:16:51.694426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e61691ae851'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column('title', sa.String(length=200), nullable=False, index=True),
        # sa.Column('content', sa.Text(), nullable=False),
        # sa.Column('published', sa.Boolean(), nullable=False),
        # sa.Column('owner_id', sa.Integer(), nullable=True),
        # sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        # sa.PrimaryKeyConstraint('id'),
        # sa.UniqueConstraint('title'),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
