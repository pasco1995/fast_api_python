"""add content col to posts table

Revision ID: 3e753edcac8b
Revises: 5f74f02a8e26
Create Date: 2022-10-26 20:09:16.011199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e753edcac8b'
down_revision = '5f74f02a8e26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
