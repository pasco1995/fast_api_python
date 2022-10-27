"""add foreign-key to posts table

Revision ID: de936a67aff7
Revises: d83bb6ce61de
Create Date: 2022-10-26 20:27:18.082189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de936a67aff7'
down_revision = 'd83bb6ce61de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
