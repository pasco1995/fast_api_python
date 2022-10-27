"""add last few cols to post table

Revision ID: 26dda373cdc2
Revises: de936a67aff7
Create Date: 2022-10-26 20:32:29.394700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26dda373cdc2'
down_revision = 'de936a67aff7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
