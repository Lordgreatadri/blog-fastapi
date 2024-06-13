"""add colums to posts table

Revision ID: 345ee227e286
Revises: 2f9523ee9d8b
Create Date: 2024-06-13 12:18:13.965850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '345ee227e286'
down_revision: Union[str, None] = '2f9523ee9d8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.Text(), nullable=False))
    op.add_column(
        "posts",sa.Column("published", sa.Boolean(), server_default='TRUE', nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    pass
