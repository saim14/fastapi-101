"""Add content column to posts table

Revision ID: 9dae55f25734
Revises: 9ae1b3e156f6
Create Date: 2021-12-01 13:48:12.428333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dae55f25734'
down_revision = '9ae1b3e156f6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
