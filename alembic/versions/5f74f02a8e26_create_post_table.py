"""create post table

Revision ID: 5f74f02a8e26
Revises: 
Create Date: 2022-10-26 19:55:09.413595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f74f02a8e26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
