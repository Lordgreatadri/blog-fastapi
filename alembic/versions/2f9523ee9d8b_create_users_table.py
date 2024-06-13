"""create users table

Revision ID: 2f9523ee9d8b
Revises: 3e61691ae851
Create Date: 2024-06-12 15:36:40.142042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f9523ee9d8b'
down_revision: Union[str, None] = '3e61691ae851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, index=True),
        sa.Column("name", sa.String(), index=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, index=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
